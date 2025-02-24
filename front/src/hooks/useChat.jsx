import { createContext, useContext, useEffect, useState } from "react";

const socket = new WebSocket("ws://127.0.0.1:8765");

const ChatContext = createContext();

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState();
  const [html, setHtml] = useState();
  const [steps, setSteps] = useState([]);
  const [through, setThrough] = useState("");
  const [loading, setLoading] = useState(false);
  const [cameraZoomed, setCameraZoomed] = useState(true);

  const chat = async (message) => {
    setLoading(true);
    socket.send(JSON.stringify({ message }));
  };

  socket.onmessage = (event) => {
    const { type, ...message } = JSON.parse(event.data);
    switch (type) {
      case "tool":
        console.log("Action called : " + message.tool);
        console.log("Used Params : " + JSON.stringify(message.tool_input));
        return;
      case "thought":
        setThrough(message.message);
        return;
      case "steps":
        setSteps(message.steps);
        return;
      case "animation":
        setMessages((messages) => [...messages, message]);
        return;
      case "display_html":
        setHtml(message.html);
        return;
      default:
        setThrough("");
        setLoading(false);
        setMessages([message]);
        return;
    }
  };

  const onMessagePlayed = () => {
    setMessages((messages) => messages.slice(1));
  };

  useEffect(() => {
    if (messages.length > 0) {
      setMessage(messages[0]);
    } else {
      setMessage(null);
    }
  }, [messages]);

  return (
    <ChatContext.Provider
      value={{
        chat,
        message,
        onMessagePlayed,
        loading,
        cameraZoomed,
        setCameraZoomed,
        through,
        html,
        steps,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error("useChat must be used within a ChatProvider");
  }
  return context;
};
