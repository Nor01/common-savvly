import { Worker } from "@react-pdf-viewer/core";
import { Viewer } from "@react-pdf-viewer/core";
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import "@react-pdf-viewer/core/lib/styles/index.css";

const PdfPreview = ({pdf}) => {
  const defaultLayoutPluginInstance = defaultLayoutPlugin();

  return (
    <>
      {!pdf && (
        <div
          style={{ height: "100%" }}
          className="is-flex is-justify-content-center is-align-items-center is-flex-direction-column"
        >
          <div className="loadingSpinner"></div>
          <p>Loading Contract Draft</p>
        </div>
      )}

      {pdf && (
        <Worker workerUrl="https://unpkg.com/pdfjs-dist@2.14.305/build/pdf.worker.min.js">
          <div
            style={{
              border: "1px solid rgba(0, 0, 0, 0.3)",
              height: "650px",
            }}
          >
            <Viewer fileUrl={pdf} plugins={[defaultLayoutPluginInstance]}/>
          </div>
        </Worker>
      )}
    </>
  );
};

export default PdfPreview;
