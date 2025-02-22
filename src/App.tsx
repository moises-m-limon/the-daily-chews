// import { useBasic, useQuery } from "@basictech/react";
// import { useState, useEffect } from "react";
// import "./App.css";
// import { BrowserAI } from "@browserai/browserai";

// const ai = new BrowserAI();

// const deleteCursorIcon = `url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM2MEE1RkEiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSIzIDYgNSA2IDIxIDYiPjwvcG9seWxpbmU+PHBhdGggZD0iTTE5IDZ2MTRhMiAyIDAgMCAxLTIgMkg3YTIgMiAwIDAgMS0yLTJWNm0zIDBWNGEyIDIgMCAwIDEgMi0yaDRhMiAyIDAgMCAxIDIgMnYyIj48L3BhdGg+PC9zdmc+),auto`;

// function App() {
//   const { db } = useBasic();
//   const emojis = useQuery(() => db.collection("emojis").getAll());
//   const { signin, isSignedIn, user, signout } = useBasic();

//   // State for AI input and response
//   const [userInput, setUserInput] = useState("");
//   const [aiResponse, setAiResponse] = useState("");
//   const [loading, setLoading] = useState(true);

//   // Load AI Model
//   useEffect(() => {
//     const loadAIModel = async () => {
//       try {
//         await ai.loadModel("llama-3.2-1b-instruct", {
//           quantization: "q4f16_1",
//         });
//         setLoading(false); // Model is loaded
//       } catch (error) {
//         console.error("Error loading AI model:", error);
//         setAiResponse("Failed to load AI model.");
//         setLoading(false);
//       }
//     };
//     loadAIModel();
//   }, []);

//   // Function to handle AI generation
//   const handleGenerateText = async () => {
//     if (!userInput.trim()) return;
//     setAiResponse("Generating response...");

//     try {
//       const response = await ai.generateText([
//         { role: "system", content: "You are a helpful assistant." },
//         { role: "user", content: userInput },
//       ]);
//       console.log(response);
//       setAiResponse(response || "No response received.");
//     } catch (error) {
//       setAiResponse("Error generating response.");
//       console.error(error);
//     }
//   };

//   return (
//     <>
//       <h1 className="text-4xl font-bold font-mono">create-lofi-app</h1>

//       {loading ? (
//         <div className="text-center mt-10">
//           <p className="text-lg font-semibold">Loading AI model...</p>
//           <p className="text-gray-500">This may take a few seconds.</p>
//         </div>
//       ) : (
//         <div className="card mt-10 p-4 border border-gray-300 rounded-lg shadow-md">
//           <h2 className="text-2xl font-bold">AI Assistant</h2>
//           <input
//             type="text"
//             className="border p-2 rounded-md w-full mt-2"
//             placeholder="Ask the AI something..."
//             value={userInput}
//             onChange={(e) => setUserInput(e.target.value)}
//             disabled={loading} // Disable input while loading
//           />
//           <button
//             className="mt-2 bg-blue-500 text-white px-4 py-2 rounded-md"
//             onClick={handleGenerateText}
//             disabled={loading} // Disable button while loading
//           >
//             {loading ? "Loading..." : "Generate Response"}
//           </button>
//           <p className="mt-4 p-2 bg-gray-100 rounded-md">{aiResponse}</p>
//         </div>
//       )}

//       <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-32 max-w-5xl mx-auto px-4">
//         <a
//           href="https://docs.basic.tech"
//           target="_blank"
//           className="card-link group"
//         >
//           <h2 className="card-title">Basic Docs</h2>
//           <p className="card-description">Auth, sync, and database</p>
//         </a>

//         <a
//           href="https://vite-pwa-org.netlify.app/"
//           target="_blank"
//           className="card-link group"
//         >
//           <h2 className="card-title">PWA Reference</h2>
//           <p className="card-description">Enable offline capabilities</p>
//         </a>

//         <a
//           href="https://tailwindcss.com/docs"
//           target="_blank"
//           className="card-link group"
//         >
//           <h2 className="card-title">Tailwind</h2>
//           <p className="card-description">Styling framework</p>
//         </a>
//       </div>
//     </>
//   );
// }

// export default App;
import { useBasic, useQuery } from "@basictech/react";
import { useState, useEffect } from "react";
import "./App.css";
import { BrowserAI } from "@browserai/browserai";

const ai = new BrowserAI();

const deleteCursorIcon = `url(data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM2MEE1RkEiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cG9seWxpbmUgcG9pbnRzPSIzIDYgNSA2IDIxIDYiPjwvcG9seWxpbmU+PHBhdGggZD0iTTE5IDZ2MTRhMiAyIDAgMCAxLTIgMkg3YTIgMiAwIDAgMS0yLTJWNm0zIDBWNGEyIDIgMCAwIDEgMi0yaDRhMiAyIDAgMCAxIDIgMnYyIj48L3BhdGg+PC9zdmc+),auto`;

function App() {
  const { db } = useBasic();
  const emojis = useQuery(() => db.collection("emojis").getAll());
  const { signin, isSignedIn, user, signout } = useBasic();

  // State for AI text generation
  const [userInput, setUserInput] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [loading, setLoading] = useState(true);

  // States for processing AI output through the backend
  const [processedSummary, setProcessedSummary] = useState("");
  const [processedAudio, setProcessedAudio] = useState("");
  const [processedImage, setProcessedImage] = useState("");
  const [processingAiOutput, setProcessingAiOutput] = useState(false);

  // Load AI Model
  useEffect(() => {
    const loadAIModel = async () => {
      try {
        await ai.loadModel("llama-3.2-1b-instruct", {
          quantization: "q4f16_1",
        });
        setLoading(false); // Model is loaded
      } catch (error) {
        console.error("Error loading AI model:", error);
        setAiResponse("Failed to load AI model.");
        setLoading(false);
      }
    };
    loadAIModel();
  }, []);

  // Function to handle AI text generation
  const handleGenerateText = async () => {
    if (!userInput.trim()) return;
    setAiResponse("Generating response...");

    try {
      const response = await ai.generateText([
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: userInput },
      ]);
      console.log(response);
      setAiResponse(response || "No response received.");
    } catch (error) {
      setAiResponse("Error generating response.");
      console.error(error);
    }
  };

  // Function to pass the AI assistant output to the backend
  const handleProcessAiOutput = async () => {
    if (!aiResponse.trim()) {
      alert("No AI output to process!");
      return;
    }
    setProcessingAiOutput(true);
    try {
      console.log(aiResponse);
      const response = await fetch("http://127.0.0.1:5000/process_article", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // Use the AI assistant output as the "article_text" for the backend
        body: JSON.stringify({ article_text: aiResponse }),
      });
      if (!response.ok) throw new Error("Failed to process AI output");

      const data = await response.json();
      setProcessedSummary(data.summary || "");
      if (data.audio) {
        setProcessedAudio(`data:audio/mp3;base64,${data.audio}`);
      }
      if (data.image) {
        setProcessedImage(`data:image/png;base64,${data.image}`);
      }
    } catch (error) {
      console.error("Error processing AI output:", error);
      setProcessedSummary("Error processing AI output.");
    } finally {
      setProcessingAiOutput(false);
    }
  };

  return (
    <>
      <h1 className="text-4xl font-bold font-mono">create-lofi-app</h1>
      <div className="card">
        <a href="/instagram">Instagram</a>
        <div className="flex flex-row gap-4 justify-center min-h-[60px] ">
          {emojis?.map((e: { id: string; value: string }) => (
            <div
              key={e.id}
              className="rounded-md m-2 p-2"
              style={{ cursor: deleteCursorIcon }}
              onClick={() => db.collection("emojis").delete(e.id)}
            >
              {e.value}
            </div>
          ))}
        </div>

        <div>
          {isSignedIn ? (
            <div>
              <p>Signed in as: {user.email}</p>
              <button onClick={signout}>Sign Out</button>
            </div>
          ) : (
            <button onClick={signin}>Sign In</button>
          )}
        </div>
      </div>
      {/* AI Text Generation Section */}
      {loading ? (
        <div className="text-center mt-10">
          <p className="text-lg font-semibold">Loading AI model...</p>
          <p className="text-gray-500">This may take a few seconds.</p>
        </div>
      ) : (
        <div className="card mt-10 p-4 border border-gray-300 rounded-lg shadow-md">
          <h2 className="text-2xl font-bold">AI Assistant</h2>
          <input
            type="text"
            className="border p-2 rounded-md w-full mt-2"
            placeholder="Ask the AI something..."
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            disabled={loading}
          />
          <button
            className="mt-2 bg-blue-500 text-white px-4 py-2 rounded-md"
            onClick={handleGenerateText}
            disabled={loading}
          >
            {loading ? "Loading..." : "Generate Response"}
          </button>
          <p className="mt-4 p-2 bg-gray-100 rounded-md">{aiResponse}</p>
        </div>
      )}
      {/* Process AI Output Section */}
      <div className="card mt-10 p-4 border border-gray-300 rounded-lg shadow-md">
        <h2 className="text-2xl font-bold">Process AI Output</h2>
        <button
          className="mt-2 bg-purple-500 text-white px-4 py-2 rounded-md"
          onClick={handleProcessAiOutput}
          disabled={processingAiOutput || !aiResponse.trim()}
        >
          {processingAiOutput ? "Processing..." : "Process AI Output"}
        </button>
        {processedSummary && (
          <div className="mt-4">
            <p className="font-bold">Summary:</p>
            <p>{processedSummary}</p>
          </div>
        )}
        {processedAudio && (
          <div className="mt-4">
            <p className="font-bold">Audio:</p>
            <audio controls src={processedAudio}></audio>
          </div>
        )}
        {processedImage && (
          <div className="mt-4">
            <p className="font-bold">Image:</p>
            <img
              src={processedImage}
              alt="Processed"
              className="mt-2 rounded-lg shadow-md"
            />
          </div>
        )}
      </div>
      {/* Footer Links */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-32 max-w-5xl mx-auto px-4">
        <a
          href="https://docs.basic.tech"
          target="_blank"
          className="card-link group"
        >
          <h2 className="card-title">Basic Docs</h2>
          <p className="card-description">Auth, sync, and database</p>
        </a>

        <a
          href="https://vite-pwa-org.netlify.app/"
          target="_blank"
          className="card-link group"
        >
          <h2 className="card-title">PWA Reference</h2>
          <p className="card-description">Enable offline capabilities</p>
        </a>

        <a
          href="https://tailwindcss.com/docs"
          target="_blank"
          className="card-link group"
        >
          <h2 className="card-title">Tailwind</h2>
          <p className="card-description">Styling framework</p>
        </a>
      </div>
    </>
  );
}

export default App;
