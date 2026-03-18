import { useState } from "react";
import "../css/dashboard.css";
import { Links } from "react-router-dom";

function Dashboard() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [isResults, setIsResults] = useState(false);
  const [isIrrelevant, setIsIrrelevant] = useState(false);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [onload,setonload] =useState(false);

  const [showUpload, setShowUpload] = useState(true);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setFile(e.dataTransfer.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file");
    if(loading) return 

    setLoading(true);
    setIsIrrelevant(false);
    setIsResults(false);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("subject", "General");

    try {
      const res = await fetch("https://globalindexsheet.onrender.com", {
        method: "POST",
        body: formData,
      });
      

      const result = await res.json();

      if (result.status === "irrelevant") {
        setMessage("❌ The uploaded file is irrelevant to the subject");
        setIsIrrelevant(true);
      } else {
        setData(result.gis);
        setIsResults(true);

        setShowUpload(false);
      }
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Something went wrong while uploading");
      setIsIrrelevant(true);
    }

    setLoading(false);
  };

  const handleNewUpload = () => {
    setFile(null);
    setData(null);
    setIsResults(false);
    setIsIrrelevant(false);
    setMessage("");
    setShowUpload(true);
  };

  return (
    <div className="container">
        <br />
        <h1>AI Powered Global Index Sheet Generator</h1><br />
      {showUpload && (
        <>
          <div
            className="upload-box"
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onClick={() => document.getElementById("fileInput").click()}
          >
            <p className="main-text">📂 Drop your file here</p>
            <p className="sub-text">or click to browse</p>

            <input
              id="fileInput"
              type="file"
              onChange={handleFileChange}
              hidden
            />

            {file && <p className="file-name">Selected: {file.name}</p>}
          </div>

          <button disabled={loading} className="upload-btn" onClick={handleUpload}>
            {loading ? "Processing" : "Upload"}
          </button>
        </>
      )}

      {!showUpload && (
        <button className="upload-btn" onClick={handleNewUpload}>
          🔄 Upload New File
        </button>
      )}

      {loading && <h3>⏳ Processing... Generating GIS...</h3>}

      {isIrrelevant && <h3 className="error-text">{message}</h3>}

      {!isIrrelevant && isResults && data && (
        <div className="table-container">
          <h3>📊 Global Index Sheet</h3>

          <table>
            <thead>
              <tr>
                <th>Grand Topic</th>
                <th>Topic</th>
                <th>Subtopic</th>
              </tr>
            </thead>

            <tbody>
              {data?.["Grand Topics"]?.flatMap((gt, i) =>
                gt.topics?.flatMap((topic, j) =>
                  topic.subtopics?.map((s, k) => (
                    <tr key={`${i}-${j}-${k}`}>
                      <td>
                        <strong>{gt.code}</strong><br />
                        {gt.name}
                      </td>

                      <td>
                        <strong>{topic.code}</strong><br />
                        {topic.name}
                        <br />
                        <small>
                          {topic.difficulty && `📊 ${topic.difficulty}`}
                          {topic.blooms_level && ` | 🧠 ${topic.blooms_level}`}
                        </small>
                      </td>

                      <td>
                        <strong>{s.code}</strong>: {s.name}
                        <br />
                        <small>
                          {s.difficulty && `📊 ${s.difficulty}`}
                          {s.blooms_level && ` | 🧠 ${s.blooms_level}`}
                        </small>

                        {s.source && (
                          <div className="source-box">
                            <small>
                              📄 {s.source.snippet}
                              <br />
                              📍 {s.source.section}
                              <br />
                              🎯 {s.source.confidence}
                            </small>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))
                )
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;