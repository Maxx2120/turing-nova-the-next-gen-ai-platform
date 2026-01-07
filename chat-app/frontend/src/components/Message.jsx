import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot } from 'lucide-react';

const Message = ({ message }) => {
    const isUser = message.sender === 'user';

    return (
        <div className={`flex w-full mb-4 ${isUser ? 'justify-end' : 'justify-start'} animate-slide-up`}>
            <div className={`flex max-w-[80%] md:max-w-[70%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-end gap-2`}>

                {/* Avatar */}
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center 
                    ${isUser ? 'bg-primary-500' : 'bg-gray-800'} text-white shadow-sm`}>
                    {isUser ? <User size={16} /> : <Bot size={16} />}
                </div>

                {/* Bubble */}
                <div className={`px-4 py-2 rounded-2xl shadow-sm text-sm md:text-base leading-relaxed break-words
                    ${isUser
                        ? 'bg-primary-500 text-white rounded-br-none'
                        : 'bg-white text-gray-800 border border-gray-100 rounded-bl-none'
                    }`}>
                    {isUser ? (
                        <p>{message.content}</p>
                    ) : (
                        <div className="prose prose-sm max-w-none dark:prose-invert">
                            <ReactMarkdown>{message.content}</ReactMarkdown>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Message;
