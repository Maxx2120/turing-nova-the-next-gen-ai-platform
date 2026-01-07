from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from llm.model_loader import get_llm
from llm.prompt_templates import get_chat_prompt_template
from llm.memory import get_session_history, persist_message
from utils.logger import logger
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableConfig
import json
import asyncio

router = APIRouter()

# Initialize LLM & Chain once (or per request if needed, but once is better for local)
try:
    llm = get_llm(model_name="llama3") # Default to llama3, can be configurable
    prompt = get_chat_prompt_template()
    
    # Create the runnable chain with history
    chain_with_history = RunnableWithMessageHistory(
        prompt | llm,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
except Exception as e:
    logger.critical(f"Critical Error Initializing LLM System: {e}")
    # We allow the app to start but the WS will fail gracefully if called
    chain_with_history = None


@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    Handles the WebSocket connection for real-time chat.
    """
    await websocket.accept()
    logger.info(f"WebSocket connected: {session_id}")

    if chain_with_history is None:
        await websocket.send_text("System Error: LLM not initialized. Check logs.")
        await websocket.close()
        return

    try:
        while True:
            # 1. Receive JSON data from client
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                user_input = payload.get("message", "")
            except json.JSONDecodeError:
                # If plain text is sent
                user_input = data

            if not user_input.strip():
                continue

            # 2. Persist User Message
            persist_message(session_id, "user", user_input)

            # 3. Stream Response
            # We use stream to give a real-time feel
            response_buffer = ""
            
            # Send a "start" signal (optional, can just start streaming text)
            # await websocket.send_json({"type": "start"})

            try:
                async for chunk in chain_with_history.astream(
                    {"input": user_input},
                    config={"configurable": {"session_id": session_id}}
                ):
                    content = chunk.content
                    if content:
                        response_buffer += content
                        # Send chunk to client
                        await websocket.send_json({
                            "type": "stream",
                            "content": content
                        })
                
                # 4. Finalize and Persist Bot Response
                persist_message(session_id, "bot", response_buffer)
                
                # Send "end" signal
                await websocket.send_json({"type": "end"})

            except Exception as e:
                logger.error(f"Error during LLM inference: {e}")
                await websocket.send_json({
                    "type": "error",
                    "content": "Sorry, I encountered an error processing that."
                })

    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"Unexpected WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass
