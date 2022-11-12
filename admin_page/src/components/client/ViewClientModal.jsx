const ViewClientModal = ({ client, closeModal, pii }) => {
    if (!client)
        return;

    return (
        <div className={"modal " + (client != null ? "is-active" : "")}>
            <div className="modal-background" />
            <div className="modal-card">
                <header className="modal-card-head">
                    <p className="modal-card-title">{client.idx} Data</p>
                    <button className="delete" aria-label="close" onClick={closeModal} />
                </header>
                <section className="modal-card-body">
                    {
                        <div className="columns is-multiline">
                            <div className="column is-6-tablet is-12-mobile">
                                <p> <strong>Account ID:</strong> {client.accountid} </p>
                                <p> <strong>Advisor assigned:</strong> {client.parentid} </p>
                                <p> <strong>Age:</strong> {client.age} </p>
                                <p> <strong>Status:</strong> {client.statusflag} </p>
                                <p> <strong>Address:</strong> {pii?.address}</p>
                                <p> <strong>Social Security:</strong> {pii?.social}</p>
                                <p> <strong>Mother Name:</strong> {pii?.mothername}</p>
                                <p> <strong>Date of Birth:</strong> {pii?.dateofbirth}</p>
                            </div>
                            <div className="column is-6-tablet is-12-mobile">
                                <p> <strong>Gender:</strong> {client.sex} </p>
                                <p> <strong>FMV:</strong> {client.fmv} </p>
                                <p> <strong>Fund:</strong> {client.fund} </p>
                                <p> <strong>Number of Shares:</strong> {client.numshares} </p>
                                <p> <strong>Number of Shares (Inheritance):</strong> {client.numshares_inheritence} </p>
                                <p> <strong>Total Profit:</strong> {client.totprofit} </p>
                                <p> <strong>Transfer Amount:</strong> {client.transferamount} </p>
                                <p> <strong>Transfer ID:</strong> {client.transferid} </p>
                            </div>
                        </div>
                    }
                </section>
                <footer className="modal-card-foot">
                    <button className="button" onClick={closeModal}>Close</button>
                </footer>
            </div>
        </div>
    )
}

export default ViewClientModal