import { useState } from "react";
import "../css/dashboard.css";

function Dashboard() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [isResults, setIsResults] = useState(false);
  const [isIrrelevant, setIsIrrelevant] = useState(false);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  // File select
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Drag drop
  const handleDrop = (e) => {
    e.preventDefault();
    setFile(e.dataTransfer.files[0]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  // Upload
  const handleUpload = async () => {
    if (!file) return alert("Please select a file");

    setLoading(true);
    setIsIrrelevant(false);
    setIsResults(false);

    const formData = new FormData();
    formData.append("file", file);
    formData.append("subject", "General");

    try {
      const res = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });

      const result = await res.json();
      console.log(result);

      if (result.status === "irrelevant") {
        setMessage("❌ The uploaded file is irrelevant to the subject");
        setIsIrrelevant(true);
      } else {
        setData(result.gis);
        setIsResults(true);
      }
    } catch (err) {
      console.error(err);
      setMessage("⚠️ Something went wrong while uploading");
      setIsIrrelevant(true);
    }

    setLoading(false);
  };

  return (
    <div className="container">

      {/* Upload Box */}
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

      {/* Upload Button */}
      <button className="upload-btn" onClick={handleUpload}>
        Upload
      </button>

      {/* Loading */}
      {loading && <h3>⏳ Processing... Generating GIS...</h3>}

      {/* Error */}
      {isIrrelevant && <h3 className="error-text">{message}</h3>}

      {/* Results */}
      {!isIrrelevant && isResults && data && (
        <div className="table-container">
          <h3>📊 Global Index Sheet</h3>

          <table>
            <thead>
              <tr>
                <th>Grand Topic</th>
                <th>Topic</th>
                <th>Subtopics</th>
              </tr>
            </thead>

            <tbody>
              {data?.["Grand Topics"]?.length > 0 ? (
                data["Grand Topics"].flatMap((gt, i) =>
                  gt.topics?.map((topic, j) => (
                    <tr key={`${i}-${j}`}>
                      
                      {/* Grand Topic */}
                      <td>
                        <strong>{gt.code}</strong> <br />
                        {gt.name}
                      </td>

                      {/* Topic */}
                      <td>
                        <strong>{topic.code}</strong> <br />
                        {topic.name}
                        <br />
                        <small>
                          {topic.difficulty && `📊 ${topic.difficulty}`}
                          {topic.blooms_level && ` | 🧠 ${topic.blooms_level}`}
                        </small>
                      </td>

                      {/* Subtopics */}
                      <td>
                        {topic.subtopics?.map((s) => (
                          <div key={s.code} className="subtopic-item">
                            <strong>{s.code}</strong>: {s.name}
                            <br />
                            <small>
                              {s.difficulty && `📊 ${s.difficulty}`}
                              {s.blooms_level && ` | 🧠 ${s.blooms_level}`}
                            </small>
                          </div>
                        ))}
                      </td>

                    </tr>
                  ))
                )
              ) : (
                <tr>
                  <td colSpan="3">No structured data generated</td>
                </tr>
              )}
            </tbody>

          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;