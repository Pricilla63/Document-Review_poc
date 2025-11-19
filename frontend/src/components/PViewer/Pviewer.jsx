// import React, { useState, useEffect, useContext } from "react";
// import PDFViewer from "../PDFViewer/PDFViewer";
// import {
//   NextOutline,
//   PreviousOutline,
//   Rotate,
//   WatsonHealthZoomPan,
//   ZoomIn,
//   ZoomOut,
//   ZoomReset,
// } from "@carbon/icons-react";
// import { Tooltip } from "carbon-components-react";
// import { UserContext } from "../../context/UserContext.jsx";

// const PViewer = ({ hoveredKey, data, setPageRenderReady }) => {
//   const { selectedDocType } = useContext(UserContext);
//   const [numPages, setNumPages] = useState(null);
//   const [pageNumber, setPageNumber] = useState(1);
//   const [zoom, setZoom] = useState(1);
//   const [rotation, setRotation] = useState(0);
//   const [isPanning, setIsPanning] = useState(false);
//   const [offset, setOffset] = useState({ x: 0, y: 0 });
//   const [PDFLoad, setPDFLoad] = useState("/sample.pdf");

//   const handleZoomIn = () => setZoom((z) => Math.min(z + 0.2, 3));
//   const handleZoomOut = () => setZoom((z) => Math.max(z - 0.2, 0.5));
//   const handleRotate = () => setRotation((r) => (r + 90) % 360);
//   const togglePan = () => setIsPanning((p) => !p);

//   useEffect(() => {
//     if (
//       hoveredKey &&
//       hoveredKey.pageNum != null &&
//       hoveredKey.pageNum !== pageNumber
//     ) {
//       setPageNumber(hoveredKey.pageNum);
//     }

//     // Cleanup: reset to page 1 when hover ends
//     // return () => {
//     //   setPageNumber(1);
//     // };
//   }, [hoveredKey?.pageNum]);

//   useEffect(() => {
//     setPageRenderReady(false);
//   }, [pageNumber]);

//   useEffect(() => {
//     handlePDFChange();
//   }, [selectedDocType]);

//   const handlePDFChange = () => {
//     switch (selectedDocType) {
//       case "Bank Statement":
//         setPDFLoad("/3188332/pdf/ic_3188332_bankstatement1.pdf");
//         break;
//       case "Paystub":
//         setPDFLoad("/3188332/pdf/ic_3188332_paystub.pdf");
//         break;
//       case "W2":
//         setPDFLoad("/3188332/pdf/ic_3188332_w2.pdf");
//         break;
//       case "Schedule E":
//         setPDFLoad("");
//         break;
//       case "Credit Report":
//         setPDFLoad("/3188332/pdf/ic_3188332_creditreport.pdf");
//         break;
//       case "VVOE":
//         setPDFLoad("");
//         break;
//       case "WVOE":
//         setPDFLoad("/3188332/pdf/ic_3188332_wvoe.pdf");
//         break;
//       case "1040":
//         setPDFLoad("/1040/pdf/31883324_1.pdf");
//         break;
//       default:
//         setPDFLoad("/3188332/pdf/ic_3188332_paystub.pdf");
//         break;
//     }
//     try {
//     } catch (ex) {
//       console.log("Error in PDFChange", ex);
//     }
//   };

//   const handleReset = () => {
//     setZoom(1);
//     setRotation(0);
//     setOffset({ x: 0, y: 0 });
//     setIsPanning(false);
//   };

//   const handleMouseDown = (e) => {
//     if (!isPanning) return;
//     const startX = e.clientX;
//     const startY = e.clientY;
//     const startOffset = { ...offset };

//     const onMouseMove = (moveEvent) => {
//       const dx = moveEvent.clientX - startX;
//       const dy = moveEvent.clientY - startY;
//       setOffset({ x: startOffset.x + dx, y: startOffset.y + dy });
//     };

//     const onMouseUp = () => {
//       window.removeEventListener("mousemove", onMouseMove);
//       window.removeEventListener("mouseup", onMouseUp);
//     };

//     window.addEventListener("mousemove", onMouseMove);
//     window.addEventListener("mouseup", onMouseUp);
//   };

//   const showResetButton =
//     zoom !== 1 || rotation !== 0 || offset.x !== 0 || offset.y !== 0;

//   return (
//     <React.Fragment>
//       <div
//         style={{
//           display: "flex",
//           gap: "1rem",
//           margin: "10px 20px",
//           alignItems: "flex-end",
//           justifyContent: "space-between",
//         }}
//       >
//         <div style={{ display: "flex", gap: "1rem" }}>
//           {/* <Tooltip autoAlign label={'Zoom In'} closeOnActivation={false}> */}
//           {/* </Tooltip> */}
//           <ZoomIn onClick={handleZoomIn} />
//           <ZoomOut onClick={handleZoomOut} />
//           <WatsonHealthZoomPan onClick={togglePan} />
//           {/* <Rotate onClick={handleRotate} /> */}
//           {showResetButton && <ZoomReset onClick={handleReset} />}
//         </div>
//         <div
//           style={{
//             // display: "flex",
//             // justifyContent: "center",
//             gap: "1rem",
//             display: "flex",
//             marginTop: "10px",
//           }}
//         >
//           <PreviousOutline
//             onClick={() => setPageNumber((p) => Math.max(p - 1, 1))}
//           />
//           <span>
//             Page {pageNumber} of {numPages}
//           </span>
//           <NextOutline
//             onClick={() => setPageNumber((p) => Math.min(p + 1, numPages))}
//           />
//         </div>
//       </div>

//       <div
//         onMouseDown={handleMouseDown}
//         style={{
//           height: "85dvh",
//           overflow: "auto",
//           position: "relative",
//           cursor: isPanning ? "grab" : "default",
//         }}
//       >
//         <div
//           style={{
//             transform: `scale(${zoom}) rotate(${rotation}deg) translate(${offset.x}px, ${offset.y}px)`,
//             transformOrigin: "top center",
//             transition: isPanning ? "none" : "transform 0.3s ease",
//           }}
//         >
//           <PDFViewer
//             file={PDFLoad}
//             numPages={numPages}
//             setNumPages={setNumPages}
//             pageNumber={pageNumber}
//             setPageNumber={setPageNumber}
//             data={data}
//             hoveredKey={hoveredKey.key}
//             scale={zoom}
//           />
//         </div>
//       </div>
//     </React.Fragment>
//   );
// };

// export default PViewer;






// import React, { useState, useEffect, useContext } from "react";
// import PDFViewer from "../PDFViewer/PDFViewer";
// import {
//   NextOutline,
//   PreviousOutline,
//   Rotate,
//   WatsonHealthZoomPan,
//   ZoomIn,
//   ZoomOut,
//   ZoomReset,
// } from "@carbon/icons-react";
// import { Tooltip } from "carbon-components-react";
// import { UserContext } from "../../context/UserContext.jsx";

// const PViewer = ({ hoveredKey, data, setPageRenderReady }) => {
//   const { selectedDocType } = useContext(UserContext);
//   const [numPages, setNumPages] = useState(null);
//   const [pageNumber, setPageNumber] = useState(1);
//   const [zoom, setZoom] = useState(1);
//   const [rotation, setRotation] = useState(0);
//   const [isPanning, setIsPanning] = useState(false);
//   const [offset, setOffset] = useState({ x: 0, y: 0 });
//   const [PDFLoad, setPDFLoad] = useState("/sample.pdf");
//   const [uploadedFile, setUploadedFile] = useState(null);

//   const handleZoomIn = () => setZoom((z) => Math.min(z + 0.2, 3));
//   const handleZoomOut = () => setZoom((z) => Math.max(z - 0.2, 0.5));
//   const handleRotate = () => setRotation((r) => (r + 90) % 360);
//   const togglePan = () => setIsPanning((p) => !p);

//   useEffect(() => {
//     if (
//       hoveredKey &&
//       hoveredKey.pageNum != null &&
//       hoveredKey.pageNum !== pageNumber
//     ) {
//       setPageNumber(hoveredKey.pageNum);
//     }
//   }, [hoveredKey?.pageNum]);

//   useEffect(() => {
//     setPageRenderReady(false);
//   }, [pageNumber]);

//   useEffect(() => {
//     handlePDFChange();
//   }, [selectedDocType]);

//   useEffect(() => {
//     // Handle uploaded file data
//     if (data?.success && data?.source_file) {
//       // For uploaded files, we'll show file info since we don't have the actual PDF file
//       // In a real implementation, you would store the file and create a URL for it
//       setUploadedFile({
//         name: data.source_file,
//         invoiceCount: data.data?.length || 0,
//         invoices: data.data || []
//       });
//     } else {
//       setUploadedFile(null);
//     }
//   }, [data]);

//   const handlePDFChange = () => {
//     switch (selectedDocType) {
//       case "Bank Statement":
//         setPDFLoad("/3188332/pdf/ic_3188332_bankstatement1.pdf");
//         break;
//       case "Paystub":
//         setPDFLoad("/3188332/pdf/ic_3188332_paystub.pdf");
//         break;
//       case "W2":
//         setPDFLoad("/3188332/pdf/ic_3188332_w2.pdf");
//         break;
//       case "Schedule E":
//         setPDFLoad("");
//         break;
//       case "Credit Report":
//         setPDFLoad("/3188332/pdf/ic_3188332_creditreport.pdf");
//         break;
//       case "VVOE":
//         setPDFLoad("");
//         break;
//       case "WVOE":
//         setPDFLoad("/3188332/pdf/ic_3188332_wvoe.pdf");
//         break;
//       case "1040":
//         setPDFLoad("/1040/pdf/31883324_1.pdf");
//         break;
//       case "Invoice":
//         // For Invoice type, we handle uploaded files
//         if (uploadedFile) {
//           setPDFLoad(null); // Clear the static PDF
//         } else {
//           setPDFLoad("/sample.pdf");
//         }
//         break;
//       default:
//         setPDFLoad("/3188332/pdf/ic_3188332_paystub.pdf");
//         break;
//     }
//   };

//   const handleReset = () => {
//     setZoom(1);
//     setRotation(0);
//     setOffset({ x: 0, y: 0 });
//     setIsPanning(false);
//   };

//   const handleMouseDown = (e) => {
//     if (!isPanning) return;
//     const startX = e.clientX;
//     const startY = e.clientY;
//     const startOffset = { ...offset };

//     const onMouseMove = (moveEvent) => {
//       const dx = moveEvent.clientX - startX;
//       const dy = moveEvent.clientY - startY;
//       setOffset({ x: startOffset.x + dx, y: startOffset.y + dy });
//     };

//     const onMouseUp = () => {
//       window.removeEventListener("mousemove", onMouseMove);
//       window.removeEventListener("mouseup", onMouseUp);
//     };

//     window.addEventListener("mousemove", onMouseMove);
//     window.addEventListener("mouseup", onMouseUp);
//   };

//   const showResetButton =
//     zoom !== 1 || rotation !== 0 || offset.x !== 0 || offset.y !== 0;

//   // Show uploaded file info when we have processed an invoice
//   if (uploadedFile) {
//     return (
//       <div
//         style={{
//           height: "85dvh",
//           display: "flex",
//           flexDirection: "column",
//         }}
//       >
//         <div
//           style={{
//             display: "flex",
//             gap: "1rem",
//             margin: "10px 20px",
//             alignItems: "flex-end",
//             justifyContent: "space-between",
//           }}
//         >
//           <div style={{ display: "flex", gap: "1rem" }}>
//             <ZoomIn onClick={handleZoomIn} />
//             <ZoomOut onClick={handleZoomOut} />
//             {showResetButton && <ZoomReset onClick={handleReset} />}
//           </div>
//           <div
//             style={{
//               display: "flex",
//               gap: "1rem",
//               marginTop: "10px",
//             }}
//           >
//             <span>📄 Processed Invoice</span>
//           </div>
//         </div>

//         <div
//           style={{
//             flex: 1,
//             display: "flex",
//             flexDirection: "column",
//             alignItems: "center",
//             justifyContent: "center",
//             padding: "20px",
//             textAlign: "center",
//             overflow: "auto"
//           }}
//         >
//           <div style={{ marginBottom: "20px" }}>
//             <h4>✅ Invoice Processed Successfully!</h4>
//             <p><strong>File:</strong> {uploadedFile.name}</p>
//             <p><strong>Invoices Found:</strong> {uploadedFile.invoiceCount}</p>
//           </div>
          
//           {/* Show processing summary for each invoice */}
//           {uploadedFile.invoices.map((invoice, index) => (
//             <div 
//               key={index}
//               style={{
//                 border: "1px solid #e0e0e0",
//                 padding: "15px",
//                 margin: "10px 0",
//                 borderRadius: "8px",
//                 backgroundColor: "#f8f9fa",
//                 width: "100%",
//                 maxWidth: "400px"
//               }}
//             >
//               <h5>Invoice #{index + 1}</h5>
//               <p><strong>Vendor:</strong> {invoice.fields?.VendorName?.value || 'N/A'}</p>
//               <p><strong>Invoice Total:</strong> {invoice.fields?.InvoiceTotal?.value || 'N/A'} {invoice.fields?.InvoiceTotal?.currency || ''}</p>
//               <p><strong>Invoice Date:</strong> {invoice.fields?.InvoiceDate?.value || 'N/A'}</p>
//               <p><strong>Customer:</strong> {invoice.fields?.CustomerName?.value || 'N/A'}</p>
//               <p><strong>Line Items:</strong> {invoice.items?.length || 0}</p>
//             </div>
//           ))}
          
//           <p style={{ color: "#6f6f6f", marginTop: "20px", fontSize: "14px" }}>
//             Note: PDF preview will be available when file storage is implemented
//           </p>
//         </div>
//       </div>
//     );
//   }

//   // Show regular PDF viewer for non-uploaded files
//   return (
//     <React.Fragment>
//       <div
//         style={{
//           display: "flex",
//           gap: "1rem",
//           margin: "10px 20px",
//           alignItems: "flex-end",
//           justifyContent: "space-between",
//         }}
//       >
//         <div style={{ display: "flex", gap: "1rem" }}>
//           <ZoomIn onClick={handleZoomIn} />
//           <ZoomOut onClick={handleZoomOut} />
//           <WatsonHealthZoomPan onClick={togglePan} />
//           {showResetButton && <ZoomReset onClick={handleReset} />}
//         </div>
//         <div
//           style={{
//             display: "flex",
//             gap: "1rem",
//             marginTop: "10px",
//           }}
//         >
//           <PreviousOutline
//             onClick={() => setPageNumber((p) => Math.max(p - 1, 1))}
//           />
//           <span>
//             Page {pageNumber} of {numPages}
//           </span>
//           <NextOutline
//             onClick={() => setPageNumber((p) => Math.min(p + 1, numPages))}
//           />
//         </div>
//       </div>

//       <div
//         onMouseDown={handleMouseDown}
//         style={{
//           height: "85dvh",
//           overflow: "auto",
//           position: "relative",
//           cursor: isPanning ? "grab" : "default",
//         }}
//       >
//         <div
//           style={{
//             transform: `scale(${zoom}) rotate(${rotation}deg) translate(${offset.x}px, ${offset.y}px)`,
//             transformOrigin: "top center",
//             transition: isPanning ? "none" : "transform 0.3s ease",
//           }}
//         >
//           <PDFViewer
//             file={PDFLoad}
//             numPages={numPages}
//             setNumPages={setNumPages}
//             pageNumber={pageNumber}
//             setPageNumber={setPageNumber}
//             data={data}
//             hoveredKey={hoveredKey.key}
//             scale={zoom}
//           />
//         </div>
//       </div>
//     </React.Fragment>
//   );
// };

// export default PViewer;



import React, { useState, useEffect, useContext } from "react";
import PDFViewer from "../PDFViewer/PDFViewer";
import {
  NextOutline,
  PreviousOutline,
  WatsonHealthZoomPan,
  ZoomIn,
  ZoomOut,
  ZoomReset,
} from "@carbon/icons-react";
import { UserContext } from "../../context/UserContext.jsx";

const PViewer = ({ hoveredKey, data, setPageRenderReady }) => {
  const { selectedDocType } = useContext(UserContext);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [zoom, setZoom] = useState(1);
  const [rotation, setRotation] = useState(0);
  const [isPanning, setIsPanning] = useState(false);
  const [offset, setOffset] = useState({ x: 0, y: 0 });
  const [PDFLoad, setPDFLoad] = useState("/sample.pdf");

  const handleZoomIn = () => setZoom((z) => Math.min(z + 0.2, 3));
  const handleZoomOut = () => setZoom((z) => Math.max(z - 0.2, 0.5));
  const togglePan = () => setIsPanning((p) => !p);

  useEffect(() => {
    if (hoveredKey?.pageNum != null && hoveredKey.pageNum !== pageNumber) {
      setPageNumber(hoveredKey.pageNum);
    }
  }, [hoveredKey?.pageNum]);

  useEffect(() => {
    setPageRenderReady(false);
  }, [pageNumber]);

  useEffect(() => {
    handlePDFChange();
  }, [selectedDocType, data]);

  const handlePDFChange = () => {
    // Priority 1: Use uploaded file URL if available
    if (data?.fileUrl) {
      setPDFLoad(data.fileUrl);
      return;
    }

    // Priority 2: Use default PDFs based on document type
    switch (selectedDocType) {
      case "Bank Statement":
        setPDFLoad("/3188332/pdf/ic_3188332_bankstatement1.pdf");
        break;
      case "Paystub":
        setPDFLoad("/3188332/pdf/ic_3188332_paystub.pdf");
        break;
      case "W2":
        setPDFLoad("/3188332/pdf/ic_3188332_w2.pdf");
        break;
      case "Credit Report":
        setPDFLoad("/3188332/pdf/ic_3188332_creditreport.pdf");
        break;
      case "WVOE":
        setPDFLoad("/3188332/pdf/ic_3188332_wvoe.pdf");
        break;
      case "1040":
        setPDFLoad("/1040/pdf/31883324_1.pdf");
        break;
      case "Invoice":
        setPDFLoad("/sample.pdf");
        break;
      default:
        setPDFLoad("/3188332/pdf/ic_3188332_paystub.pdf");
        break;
    }
  };

  const handleReset = () => {
    setZoom(1);
    setRotation(0);
    setOffset({ x: 0, y: 0 });
    setIsPanning(false);
  };

  const handleMouseDown = (e) => {
    if (!isPanning) return;
    const startX = e.clientX;
    const startY = e.clientY;
    const startOffset = { ...offset };

    const onMouseMove = (moveEvent) => {
      const dx = moveEvent.clientX - startX;
      const dy = moveEvent.clientY - startY;
      setOffset({ x: startOffset.x + dx, y: startOffset.y + dy });
    };

    const onMouseUp = () => {
      window.removeEventListener("mousemove", onMouseMove);
      window.removeEventListener("mouseup", onMouseUp);
    };

    window.addEventListener("mousemove", onMouseMove);
    window.addEventListener("mouseup", onMouseUp);
  };

  const showResetButton = zoom !== 1 || rotation !== 0 || offset.x !== 0 || offset.y !== 0;

  // Show processing info when we have uploaded data
  const showProcessingInfo = data?.success && data?.source_file;

  return (
    <div style={{ height: "100%", display: "flex", flexDirection: "column" }}>
      {/* Controls Header */}
      <div
        style={{
          display: "flex",
          gap: "1rem",
          margin: "10px 20px",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <ZoomIn onClick={handleZoomIn} style={{ cursor: "pointer" }} />
          <ZoomOut onClick={handleZoomOut} style={{ cursor: "pointer" }} />
          <WatsonHealthZoomPan 
            onClick={togglePan} 
            style={{ cursor: "pointer", color: isPanning ? "#0f62fe" : "inherit" }} 
          />
          {showResetButton && <ZoomReset onClick={handleReset} style={{ cursor: "pointer" }} />}
        </div>

        <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
          <PreviousOutline
            onClick={() => setPageNumber((p) => Math.max(p - 1, 1))}
            style={{ cursor: pageNumber > 1 ? "pointer" : "not-allowed", opacity: pageNumber > 1 ? 1 : 0.5 }}
          />
          <span>
            Page {pageNumber} of {numPages || '?'}
          </span>
          <NextOutline
            onClick={() => setPageNumber((p) => Math.min(p + 1, numPages || 1))}
            style={{ cursor: pageNumber < (numPages || 1) ? "pointer" : "not-allowed", opacity: pageNumber < (numPages || 1) ? 1 : 0.5 }}
          />
        </div>
      </div>

      {/* PDF Display Area */}
      <div
        onMouseDown={handleMouseDown}
        style={{
          flex: 1,
          overflow: "auto",
          position: "relative",
          cursor: isPanning ? "grab" : "default",
          border: "1px solid #e0e0e0",
          borderRadius: "8px",
          backgroundColor: "#fafafa",
        }}
      >
        {showProcessingInfo && (
          <div style={{
            position: "absolute",
            top: "10px",
            left: "10px",
            backgroundColor: "rgba(255,255,255,0.9)",
            padding: "8px 12px",
            borderRadius: "4px",
            fontSize: "12px",
            zIndex: 10,
            border: "1px solid #0f62fe"
          }}>
            ✅ Processed: {data.source_file}
          </div>
        )}

        <div
          style={{
            transform: `scale(${zoom}) rotate(${rotation}deg) translate(${offset.x}px, ${offset.y}px)`,
            transformOrigin: "top center",
            transition: isPanning ? "none" : "transform 0.3s ease",
            minHeight: "100%",
            display: "flex",
            justifyContent: "center",
            padding: "20px",
          }}
        >
          <PDFViewer
            file={PDFLoad}
            numPages={numPages}
            setNumPages={setNumPages}
            pageNumber={pageNumber}
            setPageNumber={setPageNumber}
            data={data}
            hoveredKey={hoveredKey?.key}
            scale={zoom}
          />
        </div>
      </div>
    </div>
  );
};

export default PViewer;