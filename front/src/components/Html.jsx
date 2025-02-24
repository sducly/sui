import { useChat } from "../hooks/useChat";

export const Html = () => {
  const { html } = useChat();

  return (
    <div
      className={`h-full grow transition-width duration-300 ease-in-out ${
        html ? "w-1/2" : "w-0"
      }`}
    >
      {html && <div dangerouslySetInnerHTML={{ __html: html }} />}
    </div>
  );
};
