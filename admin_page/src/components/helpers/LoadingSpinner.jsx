import "./LoadingSpinner.css";

const LoadingSpinner = ({show}) => {
  return (
    <div className="is-flex is-justify-content-center" style={show ? {display: "block"} : {display: "none"}} >
        <div class="lds-dual-ring"></div>
    </div>
  )
}

export default LoadingSpinner;