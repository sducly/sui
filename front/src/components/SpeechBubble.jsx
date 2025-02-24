import { Html } from "@react-three/drei";

export const SpeechBubble = ({ text, position = [1, 2, 0] }) => {
  return (
    <Html distanceFactor={3}>
      <div className="bubble">{text}</div>
    </Html>
  );
};
