import React, { useState, useRef, useEffect } from 'react';
import './ChatBox.css';
import chat_bot_icon from "./../images/chat_bot_icon.jpg";

function ChatBox() {
  const fake_response = "The server is not connected ~~";
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { text: "Hey, what can I help you today!", isBot: true },
  ]);
  const [isThinking, setIsThinking] = useState(false); // Indicator to show if the bot is thinking
  const historyRef = useRef(null); // 引用聊天历史容器

  useEffect(() => {
    // 使用 setTimeout 确保在 DOM 更新后滚动到最底部
    const scrollToBottom = () => {
      if (historyRef.current) {
        historyRef.current.scrollTop = historyRef.current.scrollHeight;
      }
    };
    scrollToBottom(); 
  }, [chatHistory]); // 当 chatHistory 发生变化时触发

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const handleKeyPress = (e) => {  // 判断按下Enter 发送内容的情况
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {  // 如果是空消息则不让发送
      addUserMessage(input);  // 更新历史信息
      setInput(''); // 重置input内容
      setIsThinking(true); // Set thinking indicator to true
      await getBotResponse(input);  // 等后端的回复
    }
  };

  const addUserMessage = (message) => {  // 更新历史信息（User Side）
    setChatHistory(prev => [...prev, { text: message, isBot: false }]);
  };

  const getBotResponse = async (userMessage) => {  // 调用后端API，取得回复
    try {
      // Add "thinking" indicator to chat history
      setChatHistory(prev => [...prev, { text: 'I am thinking ...', isBot: true }]);

      const response = await fetch('http://localhost:5000/query', {
        method: 'POST',  // Specify the POST method
        headers: {
          'Content-Type': 'application/json',  // Indicate the content type
        },
        body: JSON.stringify({ message: userMessage })  // Send the message as JSON
      });

      if (!response.ok) {  // Check if the response is okay
        throw new Error('Network response was not ok');
      }

      const data = await response.json();  // Get the response text
      let botMessage = data.response;  // Extract the response string
      botMessage = botMessage.replace(/\n/g, "<br />");
      botMessage = botMessage.replace(/(?<!\\)\*\*(.+?)\*\*/g, "<b>$1</b>");

      setIsThinking(false); // Set thinking indicator to false
      updateBotMessage(botMessage);  // Replace "thinking" message with real bot response
    } catch (error) {
      console.error("Error fetching bot response:", error);
      let botMessage = fake_response;  // Extract the response string
      botMessage = botMessage.replace(/\n/g, "<br />");
      botMessage = botMessage.replace(/(?<!\\)\*\*(.+?)\*\*/g, "<b>$1</b>");

      setIsThinking(false); // Set thinking indicator to false
      updateBotMessage(botMessage);  // Replace "thinking" message with fake response
    }
  };

  const updateBotMessage = (botMessage) => {
    setChatHistory(prev => {
      const updatedHistory = [...prev];
      // Replace the last "..." message with the real bot message
      updatedHistory[updatedHistory.length - 1] = { text: botMessage, isBot: true };
      return updatedHistory;
    });
  };

  const resetChat = () => {
    setChatHistory([{ text: "Hey, what can I help you today!", isBot: true }]);
    setIsThinking(false); // Reset thinking indicator
  };

  return (
    <div className="chatbox-container">
      <div className="chat-header">
        <img src={chat_bot_icon} className="img-avatar"/>
        <div className="text-chat">Chat Bot</div>
        <button onClick={resetChat} type="submit" className="trash-button">
          <svg viewBox="0 0 448 512" className="svgIcon"><path d="M135.2 17.7L128 32H32C14.3 32 0 46.3 0 64S14.3 96 32 96H416c17.7 0 32-14.3 32-32s-14.3-32-32-32H320l-7.2-14.3C307.4 6.8 296.3 0 284.2 0H163.8c-12.1 0-23.2 6.8-28.6 17.7zM416 128H32L53.2 467c1.6 25.3 22.6 45 47.9 45H346.9c25.3 0 46.3-19.7 47.9-45L416 128z"></path></svg>
        </button>
      </div>

      {/* Chatbox container holds both history and input fields */}
      <div className="chatbox" ref={historyRef}>
        {/* Chat history container */}
        <div className="historyChat">
          {chatHistory.map((message, index) => (
            <div key={index} className={`text ${message.isBot ? 'botText' : 'userText'}`}>
              {message.isBot ? (
                <p dangerouslySetInnerHTML={{ __html: message.text }}></p>
              ) : (
                <p>{message.text}</p>
              )}
            </div>
          ))}
        </div>
      </div>
      
      {/* Fixed input area */}
      <div className="user-input">
        <textarea
          type="text"
          name="msg"
          className="course-input"
          value={input}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here"
        />
        <button className="send-button" onClick={handleSubmit}>
          <div className="svg-wrapper-1">
            <div className="svg-wrapper">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
                <path fill="none" d="M0 0h24v24H0z"></path>
                <path fill="currentColor" d="M1.946 9.315c-.522-.174-.527-.455.01-.634l19.087-6.362c.529-.176.832.12.684.638l-5.454 19.086c-.15.529-.455.547-.679.045L12 14l6-8-8 6-8.054-2.685z"></path>
              </svg>
            </div>
          </div>
          <span>Send</span>
        </button>
      </div>
    </div>
  );
}

export default ChatBox;
