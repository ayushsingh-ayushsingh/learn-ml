import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"
import { Runner } from 'react-runner'

function App() {
  const [code, setCode] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  const fullText = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.";

  const startStreaming = () => {
    setCode("");
    setIsStreaming(true);
  };

  useEffect(() => {
    if (!isStreaming) return;

    let i = 0;
    const interval = setInterval(() => {
      setCode((prev) => prev + fullText[i]);
      i++;

      if (i >= fullText.length - 1) {
        clearInterval(interval);
        setIsStreaming(false);
      }
    }, 20);

    return () => clearInterval(interval);
  }, [isStreaming]);

  return (
    <div className="flex min-h-svh max-w-5xl mx-auto flex-col items-center justify-center p-10 gap-4">
      <Button onClick={startStreaming} disabled={isStreaming}>
        {isStreaming ? "Streaming..." : "Simulate Agent Stream"}
      </Button>

      <Runner
        code={`<div>${code}</div>`}
      />
    </div>
  )
}

export default App