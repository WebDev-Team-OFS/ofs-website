import SearchBar from './SearchBar'
import './navigation-bar.css'
import { useNavigate } from 'react-router-dom';

function NavigationBar() {
    const navigate = useNavigate();

    const goToHome = () => {
        navigate('/');
    }

    return (
        <header className="navigation-bar">
            <h1 className="logo" onClick={goToHome}>OFS</h1>
            <SearchBar />
            <div className="profile-container">
                <img className="shopping-cart-icon" src="./src/img/shopping-cart-icon.png" alt="" />
                <img className="profile-icon" src="./src/img/profile-icon.png" alt="" />
            </div>
        </header>
    )
}

export default NavigationBar;