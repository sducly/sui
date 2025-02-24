import { Loader } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { Leva } from "leva";
import { Experience } from "./components/Experience";
import { UI } from "./components/UI";
import { Html } from "./components/Html";
import TodoList from "./components/TodoList";

function App() {
  return (
    <>
      <Loader />
      <Leva hidden />
      <UI />
      <div className="flex gap-2 h-screen">
        <TodoList />
        <div className="h-full grow">
          <Canvas shadows camera={{ position: [0, 0, 1], fov: 30 }}>
            <Experience />
          </Canvas>
        </div>
      </div>
    </>
  );
}

export default App;
