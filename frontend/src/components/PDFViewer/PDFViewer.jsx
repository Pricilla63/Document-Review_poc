// import { Document, Page, pdfjs } from "react-pdf";
// import { Loading } from "@carbon/react";
// import {} from "@carbon/icons-react";

// import "react-pdf/dist/esm/Page/AnnotationLayer.css";
// import "react-pdf/dist/esm/Page/TextLayer.css";
// import "./PDFViewer.css"; // Optional for custom styles
// import { schemaMap } from "../../config/schemaMap";

// pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

// function PdfViewer({
//   file,
//   numPages,
//   setNumPages,
//   pageNumber,
//   setPageNumber,
//   data,
//   hoveredKey,
//   scale,
// }) {
//   function onDocumentLoadSuccess({ numPages }) {
//     setNumPages(numPages);
//   }

//   const renderHighlights = () => {
//     const extracted =
//       data?.extraction_json_with_coordinates || data?.extraction_json;
//     if (!extracted) return null;

//     const highlightElements = [];

//     for (const [key, val] of Object.entries(extracted)) {
//       // Case 1: It's an array like transactions or W2
//       if (Array.isArray(val)) {
//         val.forEach((item, index) => {
//           // Case 1a: Entire item has coordinates (like W2)
//           if (item?.coordinates && item?.page_num === pageNumber) {
//             const { x0, y0 } = item.coordinates;

//             // Optional: Choose a main field for ID — default to key-index
//             const primaryField =
//               schemaMap[data.doc_type]?.sectionFields?.[0] || key;

//             highlightElements.push(
//               <div
//                 key={`${primaryField}-${index}`}
//                 id={`pdf-${primaryField}-${index}`}
//                 style={{
//                   position: "absolute",
//                   left: `${x0 * 100}%`,
//                   top: `${y0 * 100}%`,
//                   width: "10px",
//                   height: "10px",
//                   backgroundColor: "transparent",
//                 }}
//               />
//             );
//           }

//           // Case 1b: Item has nested fields with coordinates (Bank Statement)
//           Object.entries(item || {}).forEach(([subKey, subVal]) => {
//             if (subVal?.coordinates && subVal?.page_num === pageNumber) {
//               const { x0, y0 } = subVal.coordinates;
//               highlightElements.push(
//                 <div
//                   key={`${subKey}-${index}`}
//                   id={`pdf-${subKey}-${index}`}
//                   style={{
//                     position: "absolute",
//                     left: `${x0 * 100}%`,
//                     top: `${y0 * 100}%`,
//                     width: "10px",
//                     height: "10px",
//                     backgroundColor: "transparent",
//                   }}
//                 />
//               );
//             }
//           });
//         });
//       }

//       // Case 2: Flat field like Employer Name
//       else if (val?.coordinates && val?.page_num === pageNumber) {
//         const { x0, y0 } = val.coordinates;
//         highlightElements.push(
//           <div
//             key={key}
//             id={`pdf-${key}`}
//             style={{
//               position: "absolute",
//               left: `${x0 * 100}%`,
//               top: `${y0 * 100}%`,
//               width: "10px",
//               height: "10px",
//               backgroundColor: "transparent",
//             }}
//           />
//         );
//       }
//     }

//     return highlightElements;
//   };

//   return (
//     <div
//       style={{
//         flex: 1,
//         // overflow: "auto",
//         display: "flex",
//         flexDirection: "column",
//         alignItems: "center",
//         justifyContent: "center",
//       }}
//     >
//       <Document
//         file={file}
//         onLoadSuccess={onDocumentLoadSuccess}
//         loading={<Loading />}
//       >
//         <div style={{ position: "relative" }}>
//           <Page
//             pageNumber={pageNumber}
//             // height={window.innerHeight - 100}
//             scale={scale || 1.5} // Default to 1.5 if not passed
//             renderAnnotationLayer={false}
//             renderTextLayer={true}
//           />
//           {renderHighlights()}
//         </div>
//       </Document>
//     </div>
//   );
// }

// export default PdfViewer;


// import { Document, Page, pdfjs } from "react-pdf";
// import { Loading } from "@carbon/react";
// import {} from "@carbon/icons-react";

// import "react-pdf/dist/esm/Page/AnnotationLayer.css";
// import "react-pdf/dist/esm/Page/TextLayer.css";
// import "./PDFViewer.css"; // Optional for custom styles

// pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

// function PdfViewer({
//   file,
//   numPages,
//   setNumPages,
//   pageNumber,
//   setPageNumber,
//   data,
//   hoveredKey,
//   scale,
// }) {
//   function onDocumentLoadSuccess({ numPages }) {
//     setNumPages(numPages);
//   }

//   // For now, we'll use a simple file display since coordinates aren't available
//   // You can enhance this later when you implement coordinate extraction

//   return (
//     <div
//       style={{
//         flex: 1,
//         display: "flex",
//         flexDirection: "column",
//         alignItems: "center",
//         justifyContent: "center",
//         minHeight: "400px",
//       }}
//     >
//       {data?.source_file ? (
//         <div style={{ textAlign: "center", padding: "20px" }}>
//           <p><strong>File:</strong> {data.source_file}</p>
//           <p><strong>Status:</strong> Processed successfully</p>
//           <p style={{ color: "#6f6f6f", marginTop: "20px" }}>
//             PDF viewer with coordinate highlighting can be implemented when coordinate data is available
//           </p>
//         </div>
//       ) : (
//         <div style={{ textAlign: "center", padding: "20px", color: "#6f6f6f" }}>
//           Upload a PDF invoice to view it here
//         </div>
//       )}
//     </div>
//   );
// }

// export default PdfViewer;




// import { Document, Page, pdfjs } from "react-pdf";
// import { Loading } from "@carbon/react";
// import {} from "@carbon/icons-react";

// import "react-pdf/dist/esm/Page/AnnotationLayer.css";
// import "react-pdf/dist/esm/Page/TextLayer.css";
// import "./PDFViewer.css"; // Optional for custom styles

// pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

// function PdfViewer({
//   file,
//   numPages,
//   setNumPages,
//   pageNumber,
//   setPageNumber,
//   data,
//   hoveredKey,
//   scale,
// }) {
//   function onDocumentLoadSuccess({ numPages }) {
//     setNumPages(numPages);
//   }

//   return (
//     <div
//       style={{
//         flex: 1,
//         display: "flex",
//         flexDirection: "column",
//         alignItems: "center",
//         justifyContent: "flex-start",
//         minHeight: "400px",
//         padding: "20px",
//         overflow: "auto",
//       }}
//     >
//       {file ? (
//         <>
//           <div style={{ marginBottom: "20px", textAlign: "center" }}>
//             <p>
//               Page {pageNumber || 1} of {numPages || 1}
//             </p>
//           </div>
//           <Document
//             file={file}
//             onLoadSuccess={onDocumentLoadSuccess}
//             loading={
//               <div style={{ textAlign: "center" }}>
//                 <Loading description="Loading PDF..." />
//                 <p>Loading PDF document...</p>
//               </div>
//             }
//             error={
//               <div style={{ textAlign: "center", color: "#ff0000" }}>
//                 <p>Error loading PDF. Please try again.</p>
//               </div>
//             }
//           >
//             <Page
//               pageNumber={pageNumber || 1}
//               scale={scale || 1.2}
//               renderAnnotationLayer={false}
//               renderTextLayer={true}
//               loading={
//                 <div style={{ textAlign: "center" }}>
//                   <Loading description="Loading page..." />
//                 </div>
//               }
//             />
//           </Document>
//           {numPages > 1 && (
//             <div style={{ marginTop: "20px", textAlign: "center" }}>
//               <p>
//                 Document has {numPages} pages. Only showing first page.
//               </p>
//             </div>
//           )}
//         </>
//       ) : data?.source_file ? (
//         <div style={{ textAlign: "center", padding: "20px" }}>
//           <p><strong>File:</strong> {data.source_file}</p>
//           <p><strong>Status:</strong> Processed successfully</p>
//           <p style={{ color: "#6f6f6f", marginTop: "20px" }}>
//             PDF file is available but not loaded for display
//           </p>
//         </div>
//       ) : (
//         <div style={{ textAlign: "center", padding: "20px", color: "#6f6f6f" }}>
//           <p>Upload a PDF invoice to view it here</p>
//           <p style={{ fontSize: "14px", marginTop: "10px" }}>
//             Select a PDF file and click "Upload and Process"
//           </p>
//         </div>
//       )}
//     </div>
//   );
// }

// export default PdfViewer;





// import { Document, Page, pdfjs } from "react-pdf";
// import { Loading } from "@carbon/react";
// import {} from "@carbon/icons-react";

// import "react-pdf/dist/esm/Page/AnnotationLayer.css";
// import "react-pdf/dist/esm/Page/TextLayer.css";
// import "./PDFViewer.css";

// pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

// function PdfViewer({
//   file,
//   numPages,
//   setNumPages,
//   pageNumber,
//   setPageNumber,
//   data,
//   hoveredKey,
//   scale,
// }) {
//   function onDocumentLoadSuccess({ numPages }) {
//     setNumPages(numPages);
//   }

//   const renderHighlights = () => {
//     if (!data) return null;

//     const extracted = 
//       data?.extraction_json_with_coordinates || 
//       data?.extraction_json || 
//       data?.analyze_result || 
//       data;

//     if (!extracted) return null;

//     const highlightElements = [];
//     let highlightId = 0;

//     const createHighlightBox = (key, value, coordinates, parentKey = '') => {
//       if (!coordinates) return null;

//       let polygon = [];
//       if (coordinates.polygon && Array.isArray(coordinates.polygon)) {
//         polygon = coordinates.polygon;
//       } else if (coordinates.x0 !== undefined && coordinates.y0 !== undefined) {
//         polygon = [
//           { x: coordinates.x0, y: coordinates.y0 },
//           { x: coordinates.x1 || coordinates.x0, y: coordinates.y1 || coordinates.y0 },
//           { x: coordinates.x2 || coordinates.x1 || coordinates.x0, y: coordinates.y2 || coordinates.y1 || coordinates.y0 },
//           { x: coordinates.x3 || coordinates.x2 || coordinates.x1 || coordinates.x0, y: coordinates.y3 || coordinates.y2 || coordinates.y1 || coordinates.y0 }
//         ];
//       } else {
//         return null;
//       }

//       const xCoords = polygon.map(p => p.x);
//       const yCoords = polygon.map(p => p.y);
      
//       const left = Math.min(...xCoords) * 100;
//       const top = Math.min(...yCoords) * 100;
//       const width = (Math.max(...xCoords) - Math.min(...xCoords)) * 100;
//       const height = (Math.max(...yCoords) - Math.min(...yCoords)) * 100;

//       if (width < 0.1 || height < 0.1) return null;

//       const fullKey = parentKey ? `${parentKey}.${key}` : key;
//       const elementId = `highlight-${fullKey}-${highlightId++}`;
//       const isHovered = hoveredKey === elementId;

//       return (
//         <div
//           key={elementId}
//           id={elementId}
//           className="pdf-highlight"
//           style={{
//             position: "absolute",
//             left: `${left}%`,
//             top: `${top}%`,
//             width: `${width}%`,
//             height: `${height}%`,
//             backgroundColor: isHovered ? "rgba(255, 255, 0, 0.4)" : "rgba(0, 123, 255, 0.3)",
//             border: `2px solid ${isHovered ? "#ff0000" : "#007bff"}`,
//             borderRadius: "3px",
//             pointerEvents: "none",
//             zIndex: 10,
//             boxShadow: isHovered ? "0 0 8px rgba(255, 0, 0, 0.6)" : "none",
//             transition: "all 0.3s ease",
//           }}
//           title={`${key}: ${JSON.stringify(value)}`}
//         />
//       );
//     };

//     const traverseObject = (obj, currentPath = '') => {
//       if (!obj || typeof obj !== 'object') return;

//       Object.entries(obj).forEach(([key, value]) => {
//         const fullPath = currentPath ? `${currentPath}.${key}` : key;

//         if (value && typeof value === 'object' && value.coordinates) {
//           const highlight = createHighlightBox(key, value, value.coordinates, currentPath);
//           if (highlight) highlightElements.push(highlight);
//         }
//         else if (Array.isArray(value)) {
//           value.forEach((item, index) => {
//             if (item && typeof item === 'object') {
//               if (item.coordinates) {
//                 const highlight = createHighlightBox(`${key}[${index}]`, item, item.coordinates, currentPath);
//                 if (highlight) highlightElements.push(highlight);
//               } else {
//                 traverseObject(item, `${fullPath}[${index}]`);
//               }
//             }
//           });
//         }
//         else if (value && typeof value === 'object') {
//           traverseObject(value, fullPath);
//         }
//       });
//     };

//     traverseObject(extracted);

//     return highlightElements;
//   };

//   return (
//     <div
//       style={{
//         flex: 1,
//         display: "flex",
//         flexDirection: "column",
//         height: "100%",
//         minHeight: "500px",
//         width: "100%",
//         overflow: "hidden",
//       }}
//     >
//       {file ? (
//         <>
//           {/* Header */}
//           <div style={{ 
//             padding: "10px 20px", 
//             borderBottom: "1px solid #e0e0e0",
//             backgroundColor: "#f8f8f8",
//             flexShrink: 0
//           }}>
//             <p style={{ margin: 0, fontWeight: "bold" }}>
//               Page {pageNumber || 1} of {numPages || 1}
//             </p>
//           </div>
          
//           {/* Main Scrollable Container */}
//           <div style={{ 
//             flex: 1,
//             width: "100%",
//             overflow: "auto",
//             backgroundColor: "#f5f5f5",
//             display: "flex",
//             justifyContent: "center",
//             padding: "20px",
//           }}>
//             {/* PDF Wrapper */}
//             <div style={{ 
//               position: "relative",
//               backgroundColor: "white",
//               border: "1px solid #ddd",
//               borderRadius: "8px",
//               boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
//               display: "inline-block", // This allows natural sizing
//               maxWidth: "100%",
//             }}>
//               <Document
//                 file={file}
//                 onLoadSuccess={onDocumentLoadSuccess}
//                 loading={
//                   <div style={{ 
//                     textAlign: "center", 
//                     padding: "60px 40px",
//                     minWidth: "300px"
//                   }}>
//                     <Loading description="Loading PDF..." />
//                     <p>Loading PDF document...</p>
//                   </div>
//                 }
//                 error={
//                   <div style={{ 
//                     textAlign: "center", 
//                     color: "#ff0000",
//                     padding: "60px 40px",
//                     minWidth: "300px"
//                   }}>
//                     <p>Error loading PDF. Please try again.</p>
//                   </div>
//                 }
//               >
//                 <Page
//                   pageNumber={pageNumber || 1}
//                   scale={scale || 1.0}
//                   renderAnnotationLayer={false}
//                   renderTextLayer={true}
//                   loading={
//                     <div style={{ 
//                       textAlign: "center", 
//                       padding: "60px 40px",
//                       minWidth: "300px"
//                     }}>
//                       <Loading description="Loading page..." />
//                     </div>
//                   }
//                 />
//               </Document>
//               {renderHighlights()}
//             </div>
//           </div>

//           {numPages > 1 && (
//             <div style={{ 
//               padding: "10px 20px", 
//               borderTop: "1px solid #e0e0e0",
//               backgroundColor: "#f8f8f8",
//               textAlign: "center",
//               flexShrink: 0
//             }}>
//               <p style={{ margin: 0, fontSize: "14px", color: "#666" }}>
//                 Document has {numPages} pages
//               </p>
//             </div>
//           )}
//         </>
//       ) : data?.source_file ? (
//         <div style={{ 
//           display: "flex",
//           flexDirection: "column",
//           justifyContent: "center",
//           alignItems: "center",
//           height: "100%",
//           padding: "40px",
//           textAlign: "center"
//         }}>
//           <p><strong>File:</strong> {data.source_file}</p>
//           <p><strong>Status:</strong> Processed successfully</p>
//           <p style={{ color: "#6f6f6f", marginTop: "20px" }}>
//             No PDF file available for display
//           </p>
//         </div>
//       ) : (
//         <div style={{ 
//           display: "flex",
//           flexDirection: "column",
//           justifyContent: "center",
//           alignItems: "center",
//           height: "100%",
//           padding: "40px",
//           textAlign: "center",
//           color: "#6f6f6f"
//         }}>
//           <p style={{ fontSize: "18px", marginBottom: "10px" }}>Upload a PDF invoice to view it here</p>
//           <p style={{ fontSize: "14px" }}>
//             Select a PDF file and click "Upload and Process"
//           </p>
//         </div>
//       )}
//     </div>
//   );
// }

// export default PdfViewer;





// import { Document, Page, pdfjs } from "react-pdf";
// import { Loading } from "@carbon/react";
// import {} from "@carbon/icons-react";

// import "react-pdf/dist/esm/Page/AnnotationLayer.css";
// import "react-pdf/dist/esm/Page/TextLayer.css";
// import "./PDFViewer.css";

// pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

// function PdfViewer({
//   file,
//   numPages,
//   setNumPages,
//   pageNumber,
//   setPageNumber,
//   data,
//   scale,
// }) {
//   function onDocumentLoadSuccess({ numPages }) {
//     setNumPages(numPages);
//   }

//   return (
//     <div
//       style={{
//         flex: 1,
//         display: "flex",
//         flexDirection: "column",
//         height: "100vh", // Use viewport height
//         width: "100%",
//         overflow: "hidden",
//       }}
//     >
//       {file ? (
//         <>
//           {/* Header - Fixed height */}
//           <div style={{ 
//             padding: "10px 20px", 
//             borderBottom: "1px solid #e0e0e0",
//             backgroundColor: "#f8f8f8",
//             flexShrink: 0,
//             height: "60px" // Fixed height
//           }}>
//             <p style={{ margin: 0, fontWeight: "bold" }}>
//               Page {pageNumber || 1} of {numPages || 1}
//             </p>
//           </div>
          
//           {/* Scrollable Area - Takes remaining space */}
//           <div style={{ 
//             flex: 1,
//             width: "100%",
//             overflow: "auto", // Scroll bars will appear here
//             backgroundColor: "#f5f5f5",
//             display: "flex",
//             justifyContent: "center",
//             alignItems: "flex-start", // Align to top
//             padding: "20px",
//             minHeight: "0", // Important for flex scrolling
//           }}>
//             {/* PDF Container */}
//             <div style={{ 
//               backgroundColor: "white",
//               border: "1px solid #ddd",
//               borderRadius: "8px",
//               boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
//               padding: "10px",
//             }}>
//               <Document
//                 file={file}
//                 onLoadSuccess={onDocumentLoadSuccess}
//                 loading={
//                   <div style={{ 
//                     textAlign: "center", 
//                     padding: "60px 40px",
//                     minWidth: "300px"
//                   }}>
//                     <Loading description="Loading PDF..." />
//                     <p>Loading PDF document...</p>
//                   </div>
//                 }
//                 error={
//                   <div style={{ 
//                     textAlign: "center", 
//                     color: "#ff0000",
//                     padding: "60px 40px",
//                     minWidth: "300px"
//                   }}>
//                     <p>Error loading PDF. Please try again.</p>
//                   </div>
//                 }
//               >
//                 <Page
//                   pageNumber={pageNumber || 1}
//                   scale={scale || 1.0}
//                   renderAnnotationLayer={false}
//                   renderTextLayer={true}
//                   loading={
//                     <div style={{ 
//                       textAlign: "center", 
//                       padding: "60px 40px",
//                     }}>
//                       <Loading description="Loading page..." />
//                     </div>
//                   }
//                 />
//               </Document>
//             </div>
//           </div>

//           {/* Footer - Fixed height */}
//           {numPages > 1 && (
//             <div style={{ 
//               padding: "10px 20px", 
//               borderTop: "1px solid #e0e0e0",
//               backgroundColor: "#f8f8f8",
//               textAlign: "center",
//               flexShrink: 0,
//               height: "50px" // Fixed height
//             }}>
//               <p style={{ margin: 0, fontSize: "14px", color: "#666" }}>
//                 Document has {numPages} pages
//               </p>
//             </div>
//           )}
//         </>
//       ) : data?.source_file ? (
//         <div style={{ 
//           display: "flex",
//           flexDirection: "column",
//           justifyContent: "center",
//           alignItems: "center",
//           height: "100%",
//           padding: "40px",
//           textAlign: "center"
//         }}>
//           <p><strong>File:</strong> {data.source_file}</p>
//           <p><strong>Status:</strong> Processed successfully</p>
//           <p style={{ color: "#6f6f6f", marginTop: "20px" }}>
//             No PDF file available for display
//           </p>
//         </div>
//       ) : (
//         <div style={{ 
//           display: "flex",
//           flexDirection: "column",
//           justifyContent: "center",
//           alignItems: "center",
//           height: "100%",
//           padding: "40px",
//           textAlign: "center",
//           color: "#6f6f6f"
//         }}>
//           <p style={{ fontSize: "18px", marginBottom: "10px" }}>Upload a PDF invoice to view it here</p>
//           <p style={{ fontSize: "14px" }}>
//             Select a PDF file and click "Upload and Process"
//           </p>
//         </div>
//       )}
//     </div>
//   );
// }

// export default PdfViewer;





import { Document, Page, pdfjs } from "react-pdf";
import { Loading } from "@carbon/react";
import {} from "@carbon/icons-react";

import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "react-pdf/dist/esm/Page/TextLayer.css";
import "./PDFViewer.css";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`;

function PdfViewer({
  file,
  numPages,
  setNumPages,
  pageNumber,
  setPageNumber,
  data,
  scale,
}) {
  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  return (
    <div
      style={{
        flex: 1,
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        width: "100%",
        overflow: "hidden",
      }}
    >
      {file ? (
        <>
          {/* Header */}
          <div style={{ 
            padding: "10px 20px", 
            borderBottom: "1px solid #e0e0e0",
            backgroundColor: "#f8f8f8",
            flexShrink: 0,
            height: "60px"
          }}>
            <p style={{ margin: 0, fontWeight: "bold" }}>
              Page {pageNumber || 1} of {numPages || 1}
            </p>
          </div>
          
          {/* MAIN CONTAINER - HORIZONTAL SCROLL BAR WILL BE AT THE BOTTOM OF THIS DIV */}
          <div style={{ 
            flex: 1,
            width: "100%",
            overflow: "auto", // ← HORIZONTAL SCROLL BAR ENABLED HERE
            backgroundColor: "#f5f5f5",
          }}>
            {/* This div allows horizontal expansion */}
            <div style={{ 
              display: "inline-block",
              minWidth: "100%",
              padding: "20px",
              boxSizing: "border-box",
            }}>
              {/* PDF Container */}
              <div style={{ 
                backgroundColor: "white",
                border: "1px solid #ddd",
                borderRadius: "8px",
                boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
                padding: "20px",
                display: "inline-block",
              }}>
                <Document
                  file={file}
                  onLoadSuccess={onDocumentLoadSuccess}
                  loading={
                    <div style={{ 
                      textAlign: "center", 
                      padding: "60px 40px",
                      minWidth: "300px"
                    }}>
                      <Loading description="Loading PDF..." />
                      <p>Loading PDF document...</p>
                    </div>
                  }
                  error={
                    <div style={{ 
                      textAlign: "center", 
                      color: "#ff0000",
                      padding: "60px 40px",
                      minWidth: "300px"
                    }}>
                      <p>Error loading PDF. Please try again.</p>
                    </div>
                  }
                >
                  <Page
                    pageNumber={pageNumber || 1}
                    scale={scale || 1.0}
                    renderAnnotationLayer={false}
                    renderTextLayer={true}
                    loading={
                      <div style={{ 
                        textAlign: "center", 
                        padding: "60px 40px",
                      }}>
                        <Loading description="Loading page..." />
                      </div>
                    }
                  />
                </Document>
              </div>
            </div>
          </div>

          {/* Footer */}
          {numPages > 1 && (
            <div style={{ 
              padding: "10px 20px", 
              borderTop: "1px solid #e0e0e0",
              backgroundColor: "#f8f8f8",
              textAlign: "center",
              flexShrink: 0,
              height: "50px"
            }}>
              <p style={{ margin: 0, fontSize: "14px", color: "#666" }}>
                Document has {numPages} pages
              </p>
            </div>
          )}
        </>
      ) : data?.source_file ? (
        <div style={{ 
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "100%",
          padding: "40px",
          textAlign: "center"
        }}>
          <p><strong>File:</strong> {data.source_file}</p>
          <p><strong>Status:</strong> Processed successfully</p>
          <p style={{ color: "#6f6f6f", marginTop: "20px" }}>
            No PDF file available for display
          </p>
        </div>
      ) : (
        <div style={{ 
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "100%",
          padding: "40px",
          textAlign: "center",
          color: "#6f6f6f"
        }}>
          <p style={{ fontSize: "18px", marginBottom: "10px" }}>Upload a PDF invoice to view it here</p>
          <p style={{ fontSize: "14px" }}>
            Select a PDF file and click "Upload and Process"
          </p>
        </div>
      )}
    </div>
  );
}

export default PdfViewer;