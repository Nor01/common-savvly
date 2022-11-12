import "./FAQ.css";
import React, { useState } from "react";

const Collapse = (props) => {
  const [state, setState] = useState({ cardState: false });

  const toggleCardState = () => {
    setState({ cardState: !state.cardState });
  };

  const { title, children } = props;
  const { cardState } = state;

  return (
    <div className="column is-12">
      <div className="card" aria-hidden={cardState ? "false" : "true"}>
        <header
          className="card-header"
          style={{ cursor: "pointer" }}
          onClick={toggleCardState}
        >
          <p className="card-header-title">{title}</p>
          <a className="card-header-icon">
            <span
              className="icon"
              style={{
                transform: cardState ? null : "rotate(180deg)",
                transition: "transform 250ms ease-out"
              }}
            >
              <i className="fa fa-angle-up"></i>
            </span>
          </a>
        </header>
        <div
          className="card-content"
          style={{
            maxHeight: cardState ? 1000 : 0,
            padding: cardState ? null : 0,
            overflow: "hidden",
            transition: "max-height 250ms ease",
            transition: "padding 250ms ease"
          }}
        >
          <div className="content">{children} </div>
        </div>
      </div>
    </div>
  );
};

const FAQ = () => {
  return (
    <div id="faqContainer" className="container p-4">
      <div className="is-flex is-justify-content-space-between">
        <h1 className="title has-text-primary">Frequently asked questions</h1>
        
      </div>
      <hr />

      <section className="section">
        <div className="container">
          <div className="is-multiline">
            <Collapse title="What makes Savvly work?">
              <p>
                Savvly is an alternative investment fund that makes risk pooling accessible to your clients. Risk pooling is the same concept behind most annuities, pension plans, and even social security —every investor contributes, and those who live the longest derive the most benefit.
              </p>
            </Collapse>
            <Collapse title="Is it insurance?">
              <p>
                No. Savvly is not an insurance policy or annuity. There is no insurance company taking profits from the Endowment Pool. Instead, that money goes to the investors who reach their Endowment Ages.
              </p>
            </Collapse>
            <Collapse title="Is it a traditional investment fund?">
              <p>
                No. Client money is invested in a brand name fund that tracks a major stock market index. Savvly does not manage this fund. It is held by a third-party custodian.
              </p>
            </Collapse>
            <Collapse title="Which accounts are eligible?">
              <p>
                Clients should use after-tax funding sources.
              </p>
            </Collapse>
            <Collapse title="When and how is the payout received?">
              <p>
                Upon reaching Endowment Age, your client will have access to fund shares equal to the principal and returns of the index fund, plus their share of the Endowment Pool in a single in-kind transfer of assets. This transfer is executed under the Limited Partnership agreement such that it is intended to be made to the client only and designed not to be assigned to anyone else.
              </p>
            </Collapse>
            <Collapse title="Can clients distribute their investments across several payout ages?">
              <p>
                Yes, as long as the total amount invested meets the minimum requirement.
              </p>
            </Collapse>
            <Collapse title="What if my client dies before payout age?">
              <p>
                Their beneficiary will receive 25% of the minimum of the initial contribution and the market value of the initial contribution less fees and expenses.
              </p>
            </Collapse>
            <Collapse title="Is there an option for couples?">
              <p>
                Couples can invest in Savvly independently as long as the total amount invested meets the minimum requirement.
              </p>
            </Collapse>
            <Collapse title="Why has nobody offered this before?">
              <p>
                Savvly has developed the proprietary AI, actuarial algorithms, and blockchain accounting to be able to accurately and equitably manage its unique Endowment Pool. Savvly was created by a team of financial industry executives, data scientists, and digital product designers. Savvly’s new model for longevity risk protection was fostered by a new wave of regulations aimed at helping Americans experience greater prosperity in retirement.
              </p>
            </Collapse>
          </div>
        </div>
      </section>


    </div>
  );
};

export default FAQ;
