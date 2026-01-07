import React from 'react';
import { useChatWebSocket } from './hooks/useChatWebSocket';
import ChatBox from './components/ChatBox';
import InputBox from './components/InputBox';
import { Sparkles } from 'lucide-react';

function App() {
    const { messages, sendMessage, isConnected, isTyping } = useChatWebSocket();

    return (
        <div className="flex flex-col h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white border-b border-gray-100 p-4 shadow-sm z-10">
                <div className="max-w-4xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="bg-primary-500 p-2 rounded-lg">
                            <Sparkles className="text-white w-5 h-5" />
                        </div>
                        <div>
                            <h1 className="font-bold text-gray-800 text-lg">AI Assistant</h1>
                            <div className="flex items-center gap-1">
                                <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-400'}`}></span>
                                <span className="text-xs text-gray-500 font-medium">
                                    {isConnected ? 'Online & Ready' : 'Connecting...'}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Chat Area */}
            <main className="flex-1 w-full max-w-4xl mx-auto bg-white shadow-xl md:my-4 md:rounded-2xl overflow-hidden flex flex-col relative border border-gray-100">
                <ChatBox messages={messages} isTyping={isTyping} />
                <InputBox onSend={sendMessage} disabled={!isConnected} />
            </main>
        </div>
    );
}

export default App;
