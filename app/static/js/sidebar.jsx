import React, { useState, useEffect } from "react";

const Sidebar = ({ apiUrl }) => {
  const [prompts, setPrompts] = useState([]);
  const [selectedPrompt, setSelectedPrompt] = useState(null);

  // Fetch prompts from the server
  useEffect(() => {
    fetch(`${apiUrl}/get-prompts`)
      .then((response) => response.json())
      .then((data) => setPrompts(data.prompts))
      .catch((error) => console.error("Error fetching prompts:", error));
  }, [apiUrl]);

  const handlePromptClick = (prompt) => {
    setSelectedPrompt(prompt);
    // Scroll or highlight the associated content if needed
    console.log("Selected Prompt:", prompt);
  };

  return (
    <div className="sidebar-container">
      <h2>Prompt Titles</h2>
      <ul className="prompt-list">
        {prompts.map((prompt) => (
          <li
            key={prompt.id}
            className={`prompt-item ${
              selectedPrompt && selectedPrompt.id === prompt.id ? "active" : ""
            }`}
            onClick={() => handlePromptClick(prompt)}
          >
            {prompt.title}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
