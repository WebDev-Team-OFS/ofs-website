import './PopUp.css'

const PopUp = ({text, closePopUp}) => {
    return (
        <div className="pop-up">
            <div>{text}</div>
            <div className="close-pop-up" onClick={closePopUp}>
                &#10005;
            </div>
        </div>
    )
}

export default PopUp;