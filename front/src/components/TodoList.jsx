import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { CheckCircle, Circle, XCircle, Loader2 } from "lucide-react";
import { useChat } from "../hooks/useChat";

const statusIcons = {
  todo: <Circle className="w-6 h-6 text-gray-400 animate-pulse" />,
  pending: <Loader2 className="w-6 h-6 text-blue-500 animate-spin" />,
  done: <CheckCircle className="w-6 h-6 text-green-500 animate-bounce" />,
  canceled: <XCircle className="w-6 h-6 text-red-500 animate-wiggle" />,
};

export default function TodoList() {
  const { steps } = useChat();

  if (!steps.length) {
    return <></>;
  }
  return (
    <div className="max-w-lg mx-auto mt-10 p-4 bg-white shadow-xl rounded-2xl">
      <h2 className="text-xl font-bold text-gray-800 mb-4">Étapes</h2>
      <ul className="space-y-4">
        {steps.map((step, index) => (
          <motion.li
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.2 }}
            className="flex items-center p-3 border rounded-lg shadow-sm"
          >
            {statusIcons[step.status]}
            <span className="ml-3 text-gray-700 font-medium">{step.step}</span>
          </motion.li>
        ))}
      </ul>
    </div>
  );
}
