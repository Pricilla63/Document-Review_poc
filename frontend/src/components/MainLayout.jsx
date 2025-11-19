// import { schemaMap } from "../config/schemaMap.js";
// import { Dropdown } from "carbon-components-react";
// import React, { useContext, useState } from "react";
// import { UserContext } from "../context/UserContext.jsx";
// import { RightPanelCloseFilled, RightPanelOpen } from "@carbon/icons-react";

// import Xarrow from "react-xarrows";
// import JViewer from "./JViewer/JViewer.jsx";
// import PViewer from "./PViewer/Pviewer.jsx";
// import GenericInputFields from "./GenericInputFields.jsx";

// const MainLayout = () => {
//   const {
//     themeStyle,
//     jsonData,
//     selectedDocType,
//     setSelectedDocType,
//     DOC_TYPES,
//   } = useContext(UserContext);

//   const [isRightPanelOpen, setIsRightPanelOpen] = useState(false);
//   const [hoveredKey, setHoveredKey] = useState({ key: null, pageNum: null });
//   const [pageRenderReady, setPageRenderReady] = useState(false);

//   const extractionData = jsonData?.extraction_json || {};

//   const toggleRightPanel = () => {
//     setIsRightPanelOpen((prev) => !prev);
//   };

//   const displayContent = (type) => {
//     const schema = schemaMap[type];
//     if (!schema)
//       return (
//         <div
//           style={{
//             padding: "10px 20px",
//           }}
//         >
//           <p>We are working on this document type</p>
//         </div>
//       );

//     return (
//       <GenericInputFields
//         data={jsonData}
//         schema={schema}
//         setHoveredKey={setHoveredKey}
//       />
//     );
//   };

//   return (
//     <div
//       className="flex flex-col md:flex-row gap-4 p-4 bg-gray-50 overflow-hidden"
//       style={{
//         padding: "10px 20px",
//         // marginTop: "3%" "To hide the header"
//       }}
//     >
//       {/* Left Side - PViewer */}
//       <div className="w-full md:w-1/2">
//         {/* <div className="flex flex-row justify-between items-center mb-2 px-2">
//           <p>
//             Loan ID: <b style={{ color: themeStyle.primary }}>{"9014960"}</b>
//           </p>
//           <p>
//             Borrower Name:{" "}
//             <b style={{ color: themeStyle.primary }}>
//               {extractionData?.["Account Holder"] || "BOWWEN F DIAMOND"}
//             </b>
//           </p>
//         </div> */}

//         <div className="border rounded-2xl shadow-md p-4 bg-white">
//           <PViewer
//             hoveredKey={hoveredKey}
//             data={jsonData}
//             setPageRenderReady={setPageRenderReady}
//           />
//         </div>
//       </div>

//       {/* Right Side - InputFields and Optional JViewer */}
//       <div className="w-full md:w-1/2 flex flex-row gap-4">
//         {/* Left side of the split - InputFields */}
//         <div
//           className={`transition-all duration-300 ${
//             isRightPanelOpen ? "w-1/2" : "w-full"
//           }`}
//         >
//           <div className="flex justify-end mb-2 pr-2">
//             {!isRightPanelOpen ? (
//               <RightPanelOpen
//                 size={24}
//                 onClick={toggleRightPanel}
//                 className="cursor-pointer"
//               />
//             ) : (
//               <RightPanelCloseFilled
//                 size={24}
//                 onClick={toggleRightPanel}
//                 className="cursor-pointer"
//               />
//             )}
//           </div>
//           <div
//             className="border rounded-2xl shadow-md p-4 bg-white"
//             style={{ height: "85dvh", marginTop: "1%", overflowY: "auto" }}
//           >
//             <div
//               style={{
//                 padding: "10px 20px",
//               }}
//             >
//               <Dropdown
//                 id="inline"
//                 titleText="Document Type"
//                 initialSelectedItem={selectedDocType}
//                 label={selectedDocType}
//                 items={DOC_TYPES}
//                 onChange={({ selectedItem }) =>
//                   setSelectedDocType(selectedItem)
//                 }
//               />
//             </div>
//             {displayContent(selectedDocType)}
//           </div>
//         </div>

//         {/* Right panel - JViewer */}
//         {isRightPanelOpen && (
//           <div
//             className="w-1/2 border rounded-2xl shadow-md p-4 bg-white transition-all duration-300"
//             style={{ height: "100%" }}
//           >
//             <JViewer data={jsonData} />
//           </div>
//         )}
//       </div>

//       {/* Arrow between JSON and PDF */}
//       {hoveredKey.key && (
//         <Xarrow
//           start={`json-${hoveredKey.key}`}
//           end={`pdf-${hoveredKey.key}`}
//           color={themeStyle.primary}
//           strokeWidth={2}
//         />
//       )}
//     </div>
//   );
// };

// export default MainLayout;



// import { schemaMap } from "../config/schemaMap.js";
// import { Dropdown, FileUploader, Button } from "carbon-components-react";
// import React, { useContext, useState } from "react";
// import { UserContext } from "../context/UserContext.jsx";
// import { RightPanelCloseFilled, RightPanelOpen } from "@carbon/icons-react";

// import Xarrow from "react-xarrows";
// import JViewer from "./JViewer/JViewer.jsx";
// import PViewer from "./PViewer/Pviewer.jsx";
// import GenericInputFields from "./GenericInputFields.jsx";

// const MainLayout = () => {
//   const {
//     themeStyle,
//     jsonData,
//     selectedDocType,
//     setSelectedDocType,
//     DOC_TYPES,
//     setJsonData,
//   } = useContext(UserContext);

//   const [isRightPanelOpen, setIsRightPanelOpen] = useState(false);
//   const [hoveredKey, setHoveredKey] = useState({ key: null, pageNum: null });
//   const [pageRenderReady, setPageRenderReady] = useState(false);
//   const [isProcessing, setIsProcessing] = useState(false);
//   const [selectedFile, setSelectedFile] = useState(null);

//   const extractionData = jsonData?.data?.[0]?.fields || {};

//   const toggleRightPanel = () => {
//     setIsRightPanelOpen((prev) => !prev);
//   };

//   const handleFileSelect = (event) => {
//     const file = event.target.files[0];
//     if (file) {
//       setSelectedFile(file);
//     }
//   };

//   const handleFileUpload = async () => {
//     if (!selectedFile) {
//       alert('Please select a file first');
//       return;
//     }

//     if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
//       alert('Please upload a PDF file');
//       return;
//     }

//     setIsProcessing(true);
    
//     const formData = new FormData();
//     formData.append('file', selectedFile);

//     try {
//       console.log('Starting upload for file:', selectedFile.name);
      
//       // Test backend connection first
//       const healthResponse = await fetch('http://localhost:5000/health');
//       console.log('Health check status:', healthResponse.status);
      
//       if (!healthResponse.ok) {
//         throw new Error('Backend health check failed');
//       }

//       // Upload the file
//       const response = await fetch('http://localhost:5000/upload', {
//         method: 'POST',
//         body: formData,
//         // Don't set Content-Type header for FormData - browser will set it automatically
//       });

//       console.log('Upload response status:', response.status);
//       console.log('Upload response headers:', response.headers);
      
//       if (!response.ok) {
//         const errorText = await response.text();
//         console.error('Server error response:', errorText);
//         throw new Error(`Server error: ${response.status} - ${errorText}`);
//       }

//       const result = await response.json();
//       console.log('Backend response data:', result);
      
//       if (result.success) {
//         setJsonData(result);
//         setSelectedDocType('Invoice');
//         console.log('File processed successfully!');
//         // Clear the selected file after successful upload
//         setSelectedFile(null);
//         // Reset file input
//         document.getElementById('file-input').value = '';
//       } else {
//         alert(`Processing error: ${result.message || 'Unknown error'}`);
//       }
//     } catch (error) {
//       console.error('Upload error details:', error);
//       alert(`Upload failed: ${error.message}\n\nPlease check:\n1. Backend is running on port 5000\n2. No CORS issues\n3. File is a valid PDF`);
//     } finally {
//       setIsProcessing(false);
//     }
//   };

//   const displayContent = (type) => {
//     const schema = schemaMap[type];
//     if (!schema)
//       return (
//         <div style={{ padding: "10px 20px" }}>
//           <p>We are working on this document type</p>
//         </div>
//       );

//     return (
//       <GenericInputFields
//         data={jsonData}
//         schema={schema}
//         setHoveredKey={setHoveredKey}
//       />
//     );
//   };

//   return (
//     <div
//       className="flex flex-col md:flex-row gap-4 p-4 bg-gray-50 overflow-hidden"
//       style={{
//         padding: "10px 20px",
//       }}
//     >
//       {/* Left Side - PViewer */}
//       <div className="w-full md:w-1/2">
//         {/* Upload Section */}
//         <div className="mb-4 p-4 border rounded-lg bg-white">
//           <h4 style={{ marginBottom: '15px', color: '#393939' }}>Upload Invoice PDF</h4>
          
//           <div style={{ marginBottom: '10px' }}>
//             <input
//               id="file-input"
//               type="file"
//               accept=".pdf"
//               onChange={handleFileSelect}
//               disabled={isProcessing}
//               style={{ marginBottom: '10px' }}
//             />
//           </div>
          
//           {selectedFile && (
//             <div style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f4f4f4', borderRadius: '4px' }}>
//               <strong>Selected file:</strong> {selectedFile.name}
//             </div>
//           )}
          
//           <Button
//             kind="primary"
//             onClick={handleFileUpload}
//             disabled={!selectedFile || isProcessing}
//           >
//             {isProcessing ? 'Processing...' : 'Upload and Process'}
//           </Button>
          
//           {isProcessing && (
//             <div style={{ marginTop: '10px', color: '#0f62fe' }}>
//               ⏳ Processing invoice... This may take a few seconds.
//             </div>
//           )}
//         </div>

//         <div className="border rounded-2xl shadow-md p-4 bg-white">
//           <PViewer
//             hoveredKey={hoveredKey}
//             data={jsonData}
//             setPageRenderReady={setPageRenderReady}
//           />
//         </div>
//       </div>

//       {/* Right Side - InputFields and Optional JViewer */}
//       <div className="w-full md:w-1/2 flex flex-row gap-4">
//         {/* Left side of the split - InputFields */}
//         <div
//           className={`transition-all duration-300 ${
//             isRightPanelOpen ? "w-1/2" : "w-full"
//           }`}
//         >
//           <div className="flex justify-end mb-2 pr-2">
//             {!isRightPanelOpen ? (
//               <RightPanelOpen
//                 size={24}
//                 onClick={toggleRightPanel}
//                 className="cursor-pointer"
//               />
//             ) : (
//               <RightPanelCloseFilled
//                 size={24}
//                 onClick={toggleRightPanel}
//                 className="cursor-pointer"
//               />
//             )}
//           </div>
//           <div
//             className="border rounded-2xl shadow-md p-4 bg-white"
//             style={{ height: "85dvh", marginTop: "1%", overflowY: "auto" }}
//           >
//             <div style={{ padding: "10px 20px" }}>
//               <Dropdown
//                 id="inline"
//                 titleText="Document Type"
//                 initialSelectedItem={selectedDocType}
//                 label={selectedDocType}
//                 items={DOC_TYPES}
//                 onChange={({ selectedItem }) => setSelectedDocType(selectedItem)}
//               />
//             </div>
//             {jsonData?.success ? (
//               displayContent(selectedDocType)
//             ) : (
//               <div style={{ padding: "20px", textAlign: "center", color: "#6f6f6f" }}>
//                 {selectedFile ? 'Click "Upload and Process" to extract data' : 'Select a PDF invoice to get started'}
//               </div>
//             )}
//           </div>
//         </div>

//         {/* Right panel - JViewer */}
//         {isRightPanelOpen && (
//           <div
//             className="w-1/2 border rounded-2xl shadow-md p-4 bg-white transition-all duration-300"
//             style={{ height: "100%" }}
//           >
//             <JViewer data={jsonData} />
//           </div>
//         )}
//       </div>

//       {/* Arrow between JSON and PDF */}
//       {hoveredKey.key && (
//         <Xarrow
//           start={`json-${hoveredKey.key}`}
//           end={`pdf-${hoveredKey.key}`}
//           color={themeStyle.primary}
//           strokeWidth={2}
//         />
//       )}
//     </div>
//   );
// };

// export default MainLayout;



import { schemaMap } from "../config/schemaMap.js";
import { Dropdown, Button } from "carbon-components-react";
import React, { useContext, useState } from "react";
import { UserContext } from "../context/UserContext.jsx";
import { RightPanelCloseFilled, RightPanelOpen } from "@carbon/icons-react";

import Xarrow from "react-xarrows";
import JViewer from "./JViewer/JViewer.jsx";
import PViewer from "./PViewer/Pviewer.jsx";
import GenericInputFields from "./GenericInputFields.jsx";

const MainLayout = () => {
  const {
    themeStyle,
    jsonData,
    setJsonData,
    selectedDocType,
    setSelectedDocType,
    DOC_TYPES,
  } = useContext(UserContext);

  const [isRightPanelOpen, setIsRightPanelOpen] = useState(false);
  const [hoveredKey, setHoveredKey] = useState({ key: null, pageNum: null });
  const [pageRenderReady, setPageRenderReady] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);

  const extractionData = jsonData?.data?.[0]?.fields || {};

  const toggleRightPanel = () => {
    setIsRightPanelOpen((prev) => !prev);
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleFileUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first');
      return;
    }

    if (!selectedFile.name.toLowerCase().endsWith('.pdf')) {
      alert('Please upload a PDF file');
      return;
    }

    setIsProcessing(true);
    
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      console.log('Starting upload for file:', selectedFile.name);
      
      // Create a URL for the file to display it immediately
      const fileUrl = URL.createObjectURL(selectedFile);
      
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      console.log('Response status:', response.status);
      
      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Server error (${response.status}): ${errorText}`);
      }

      const result = await response.json();
      console.log('Backend response:', result);
      
      if (result.success) {
        // Add the file URL to the result so PViewer can display it
        const resultWithFile = {
          ...result,
          fileUrl: fileUrl,
          uploadedFileName: selectedFile.name
        };
        setJsonData(resultWithFile);
        setSelectedDocType('Invoice');
        console.log('✅ File processed successfully!');
        setSelectedFile(null);
        document.getElementById('file-input').value = '';
      } else {
        alert(`Processing failed: ${result.message || 'Unknown error'}`);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert(`Upload failed: ${error.message}\n\nPlease check if the backend is running on port 5000.`);
    } finally {
      setIsProcessing(false);
    }
  };

  const displayContent = (type) => {
    const schema = schemaMap[type];
    if (!schema)
      return (
        <div style={{ padding: "10px 20px" }}>
          <p>We are working on this document type</p>
        </div>
      );

    return (
      <GenericInputFields
        data={jsonData}
        schema={schema}
        setHoveredKey={setHoveredKey}
      />
    );
  };

  return (
    <div
      className="flex flex-col md:flex-row gap-4 p-4 bg-gray-50 overflow-hidden"
      style={{
        padding: "10px 20px",
      }}
    >
      {/* Left Side - PViewer */}
      <div className="w-full md:w-1/2">
        {/* Upload Section */}
        <div className="mb-4 p-4 border rounded-lg bg-white">
          <h4 style={{ marginBottom: '15px', color: '#393939' }}>Upload Invoice PDF</h4>
          
          <div style={{ marginBottom: '10px' }}>
            <input
              id="file-input"
              type="file"
              accept=".pdf"
              onChange={handleFileSelect}
              disabled={isProcessing}
              style={{ marginBottom: '10px' }}
            />
          </div>
          
          {selectedFile && (
            <div style={{ marginBottom: '10px', padding: '10px', backgroundColor: '#f4f4f4', borderRadius: '4px' }}>
              <strong>Selected file:</strong> {selectedFile.name}
            </div>
          )}
          
          <Button
            kind="primary"
            onClick={handleFileUpload}
            disabled={!selectedFile || isProcessing}
          >
            {isProcessing ? 'Processing...' : 'Upload and Process'}
          </Button>
          
          {isProcessing && (
            <div style={{ marginTop: '10px', color: '#0f62fe' }}>
              ⏳ Processing invoice... This may take a few seconds.
            </div>
          )}
        </div>

        <div className="border rounded-2xl shadow-md p-4 bg-white">
          <PViewer
            hoveredKey={hoveredKey}
            data={jsonData}
            setPageRenderReady={setPageRenderReady}
          />
        </div>
      </div>

      {/* Right Side - InputFields and Optional JViewer */}
      <div className="w-full md:w-1/2 flex flex-row gap-4">
        {/* Left side of the split - InputFields */}
        <div
          className={`transition-all duration-300 ${
            isRightPanelOpen ? "w-1/2" : "w-full"
          }`}
        >
          <div className="flex justify-end mb-2 pr-2">
            {!isRightPanelOpen ? (
              <RightPanelOpen
                size={24}
                onClick={toggleRightPanel}
                className="cursor-pointer"
              />
            ) : (
              <RightPanelCloseFilled
                size={24}
                onClick={toggleRightPanel}
                className="cursor-pointer"
              />
            )}
          </div>
          <div
            className="border rounded-2xl shadow-md p-4 bg-white"
            style={{ height: "85dvh", marginTop: "1%", overflowY: "auto" }}
          >
            <div style={{ padding: "10px 20px" }}>
              <Dropdown
                id="inline"
                titleText="Document Type"
                initialSelectedItem={selectedDocType}
                label={selectedDocType}
                items={DOC_TYPES}
                onChange={({ selectedItem }) => setSelectedDocType(selectedItem)}
              />
            </div>
            {jsonData?.success ? (
              displayContent(selectedDocType)
            ) : (
              <div style={{ padding: "20px", textAlign: "center", color: "#6f6f6f" }}>
                {selectedFile ? 'Click "Upload and Process" to extract data' : 'Select a PDF invoice to get started'}
              </div>
            )}
          </div>
        </div>

        {/* Right panel - JViewer */}
        {isRightPanelOpen && (
          <div
            className="w-1/2 border rounded-2xl shadow-md p-4 bg-white transition-all duration-300"
            style={{ height: "100%" }}
          >
            <JViewer data={jsonData} />
          </div>
        )}
      </div>

      {/* Arrow between JSON and PDF */}
      {hoveredKey.key && (
        <Xarrow
          start={`json-${hoveredKey.key}`}
          end={`pdf-${hoveredKey.key}`}
          color={themeStyle.primary}
          strokeWidth={2}
        />
      )}
    </div>
  );
};

export default MainLayout;