import React, { useState } from 'react';
import './ChatBox.css';

function ChatBox() {
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { text: "Hey, what can I help you today!", isBot: true },
    { text: "User input", isBot: false },
    { text: "Server response", isBot: true },
    { text: "User input 2", isBot: false },
    { text: "User lots of input User lots of input User lots of input User lots of input User lots of input User lots of input User lots of input User lots of input User lots of input User lots of input User lots of input User lots of input User lots of inputUser lots of input User lots of input User lots of input User lots of inputUser lots of inputUser lots of inputUser lots of input", isBot: false },
  ]);

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      addUserMessage(input);
      setInput('');
      await getBotResponse(input);
    }
  };

  const addUserMessage = (message) => {
    setChatHistory(prev => [...prev, { text: message, isBot: false }]);
  };

  const getBotResponse = async (userMessage) => {
    // Mock response instead of fetching from server
    const fakeResponse = "This is a mock response to your input: " + userMessage;
    // Simulate delay to mimic API response time
    setTimeout(() => {
      setChatHistory(prev => [...prev, { text: fakeResponse, isBot: true }]);
    }, 500);

    // try {
    //   const response = await fetch(`/get?msg=${encodeURIComponent(userMessage)}`);
    //   const data = await response.text();
    //   setChatHistory(prev => [...prev, { text: data, isBot: true }]);
    // } catch (error) {
    //   console.error("Error fetching bot response:", error);
    // }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  const resetChat = () => {
    setChatHistory([]);
  };

  return (
    <div className="input-container">
      <div className="chatbox">
        <div id="historyChat">
          {chatHistory.map((message, index) => (
            <div key={index} className={`text ${message.isBot ? 'botText' : 'userText'}`}>
              <p>{message.text}</p>
            </div>
          ))}
        </div>

        <div id="userInput">
          <textarea
            id="textInput"
            type="text"
            name="msg"
            className="course-input"
            value={input}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="Type your response..."
          />
          <button id="resetButton" onClick={resetChat} type="submit" className="button">
            <div className="blob1"></div>
            <div className="blob2"></div>
            <div className="inner">Clean Conversation</div>
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatBox;

