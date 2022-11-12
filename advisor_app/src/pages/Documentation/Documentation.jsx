import { client_brochure,private_placement_memo,subscription_agreement,funding_instructions } from "../../assets/images";
import BrochurePdf from "../../assets/pdf/Brochure_Adviser_version_18_2_.pdf";
import MemorandumPdf from "../../assets/pdf/PrivatePlacementMemorandum.pdf";
import SubscriptionAgreementPdf from "../../assets/pdf/SubscriptionAgreementTemplate.pdf";
import FundingInstructionsPdf from "../../assets/pdf/How_fund_Savvly_account.pdf";


import AllFiles from "../../assets/pdf/Savvly_PDF_Files.zip";
import "./Documentation.css";

const Documentation = () => {
    return (
        <div id="docContainer" className="container p-4">
            <div className="is-flex is-justify-content-space-between">
                <h1 className="title has-text-primary">Documentation</h1>
                <div className="buttons">
                    <a
                        className="button is-primary is-outlined"
                        href={AllFiles}
                        download="Savvly_PDF_Files.zip"
                    >
                        Download All
                    </a>
                    <button className="button is-primary" onClick={() => window.open("https://calendly.com/meet-savvly/discovery?utm_medium=website&utm_source=adviser&utm_content=hero", '_blank', 'noopener,noreferrer')}>Request a Meeting</button>
                </div>
            </div>
            <hr />

            <div className="columns brochures">
                <div className="column">
                    <a href={BrochurePdf} target="_blank">
                        <img src={client_brochure} alt="" className="is-clickable" />
                    </a>
                    <div>
                        <p>Client Brochure</p>
                    </div>
                </div>
                <div className="column">
                    <a href={MemorandumPdf} target="_blank">
                        <img src={private_placement_memo} alt="" className="is-clickable" />
                    </a>
                    <div>
                        <p>Private Placement Memorandum</p>
                    </div>
                </div>
                <div className="column">
                    <a href={FundingInstructionsPdf} target="_blank">
                        <img src={funding_instructions} alt="" className="is-clickable" />
                    </a>
                    <div>
                        <p>Savvly Funding Instructions</p>
                    </div>
                </div>

                <div className="column">
                    <a href={SubscriptionAgreementPdf} target="_blank">
                        <img src={subscription_agreement} alt="" className="is-clickable" />
                    </a>
                    <div>
                        <p>Subscription Agreement template</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Documentation;
