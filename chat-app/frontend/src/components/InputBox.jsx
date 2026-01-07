import React, { useState } from 'react';
import { SendHorizontal } from 'lucide-react';

const InputBox = ({ onSend, disabled }) => {
    const [text, setText] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (text.trim() && !disabled) {
            onSend(text);
            setText('');
        }
    };

    return (
        <div className="border-t border-gray-100 bg-white p-4">
            <form onSubmit={handleSubmit} className="relative max-w-4xl mx-auto flex items-center gap-2">
                <input
                    type="text"
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    placeholder="Type a message..."
                    disabled={disabled}
                    className="w-full bg-gray-50 border border-gray-200 text-gray-900 text-sm rounded-full focus:ring-primary-500 focus:border-primary-500 block pl-4 p-3 shadow-sm transition-all outline-none disabled:opacity-50"
                />
                <button
                    type="submit"
                    disabled={!text.trim() || disabled}
                    className="bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white rounded-full p-3 shadow-md transition-all flex-shrink-0"
                >
                    <SendHorizontal size={20} />
                </button>
            </form>
        </div>
    );
};

export default InputBox;
