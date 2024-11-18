import SearchBar from './SearchBar'
import ProfileButton from './ProfileButton';
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
                <ProfileButton />
            </div>
        </header>
    )
}

export default NavigationBar;