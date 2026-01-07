import React, { useEffect, useRef } from 'react';
import Message from './Message';

const ChatBox = ({ messages, isTyping }) => {
    const bottomRef = useRef(null);

    // Auto-scroll to bottom on new message
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages, isTyping]);

    return (
        <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6 scrollbar-hide">
            {messages.length === 0 ? (
                <div className="h-full flex flex-col items-center justify-center text-gray-400 space-y-4 opacity-50">
                    <div className="bg-gray-100 p-6 rounded-full">
                        <span className="text-4xl">👋</span>
                    </div>
                    <p className="text-lg font-medium">Say hello to start chatting!</p>
                </div>
            ) : (
                messages.map((msg, idx) => (
                    <Message key={idx} message={msg} />
                ))
            )}

            {/* Simple Typing Indicator */}
            {isTyping && (
                <div className="flex justify-start animate-pulse">
                    <div className="bg-gray-200 text-gray-500 text-xs px-3 py-1 rounded-full ml-10">
                        AI is typing...
                    </div>
                </div>
            )}

            <div ref={bottomRef} />
        </div>
    );
};

export default ChatBox;
