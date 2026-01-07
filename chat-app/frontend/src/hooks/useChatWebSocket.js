import { useState, useEffect, useRef, useCallback } from 'react';
import { v4 as uuidv4 } from 'uuid';

const WS_URL = 'ws://localhost:8000/ws';

export const useChatWebSocket = () => {
    const [messages, setMessages] = useState([]);
    const [isConnected, setIsConnected] = useState(false);
    const [isTyping, setIsTyping] = useState(false);
    const ws = useRef(null);
    const sessionId = useRef(uuidv4()); // Generate session ID once per load

    useEffect(() => {
        // Connect Logic
        const connect = () => {
            const socketUrl = `${WS_URL}/${sessionId.current}`;
            ws.current = new WebSocket(socketUrl);

            ws.current.onopen = () => {
                console.log('Connected to WebSocket');
                setIsConnected(true);
            };

            ws.current.onclose = () => {
                console.log('Disconnected from WebSocket');
                setIsConnected(false);
                // Simple reconnect logic could go here
                setTimeout(connect, 3000);
            };

            ws.current.onerror = (error) => {
                console.error('WebSocket Error:', error);
            };

            ws.current.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };
        };

        connect();

        return () => {
            if (ws.current) ws.current.close();
        };
    }, []);

    const handleMessage = (data) => {
        if (data.type === 'stream') {
            setIsTyping(false);
            setMessages(prev => {
                const lastMsg = prev[prev.length - 1];

                // If the last message is from bot and we are streaming, append to it
                if (lastMsg && lastMsg.sender === 'bot' && lastMsg.isStreaming) {
                    return [
                        ...prev.slice(0, -1),
                        { ...lastMsg, content: lastMsg.content + data.content }
                    ];
                } else {
                    // New bot message block (shouldn't happen often if logic is right)
                    return [...prev, { sender: 'bot', content: data.content, isStreaming: true }];
                }
            });
        } else if (data.type === 'end') {
            setMessages(prev => {
                const lastMsg = prev[prev.length - 1];
                if (lastMsg) {
                    return [
                        ...prev.slice(0, -1),
                        { ...lastMsg, isStreaming: false }
                    ];
                }
                return prev;
            });
        } else if (data.type === 'error') {
            setIsTyping(false);
            setMessages(prev => [...prev, { sender: 'bot', content: data.content, isError: true }]);
        }
    };

    const sendMessage = useCallback((text) => {
        if (ws.current && ws.current.readyState === WebSocket.OPEN) {
            // Optimistic UI Update
            const userMsg = { sender: 'user', content: text };
            setMessages(prev => [...prev, userMsg]);

            // Prepare for Bot Response
            setIsTyping(true);

            // Add a placeholder bot message for streaming to target
            setMessages(prev => [...prev, { sender: 'bot', content: '', isStreaming: true }]);

            ws.current.send(JSON.stringify({ message: text }));
        } else {
            console.error('WebSocket is not connected');
        }
    }, []);

    return { messages, sendMessage, isConnected, isTyping };
};
