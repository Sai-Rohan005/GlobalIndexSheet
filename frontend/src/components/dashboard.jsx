import { useState } from "react";
import "../css/dashboard.css"

function Dashboard() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [isResults, setIsResults] = useState(false);
  const [isirrevelent, setisirrevelent] = useState(false);
  const [message,setmessage] = useState("");
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

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    const result = await res.json();
    console.log(result)
    if(result.status=="irrelevant"){
        setmessage("The File uploaded is irrelevant to Studies")
        setisirrevelent(true)
        setIsResults(false)
    }else{
        setisirrevelent(false)
        setData(result.gis || result);
        setIsResults(true);
    }
  };

  return (
    <div className="container">
      
      <div 
        className="upload-box"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => document.getElementById("fileInput").click()}
        >
        <p className="main-text"> Drop your file here</p>
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
        {isirrevelent && 
            <h3>{message}</h3>

        }
      {/* Results */}
      {!isirrevelent && isResults && data && (
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
              {data["Grand Topics"]?.map((gt, i) =>
                gt.topics.map((topic, j) => (
                  <tr key={`${i}-${j}`}>
                    <td>{gt.name}</td>
                    <td>{topic.name}</td>
                    <td>{topic.subtopics.join(", ")}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;