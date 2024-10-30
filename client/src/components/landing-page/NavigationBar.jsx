import SearchBar from './SearchBar'

function NavigationBar() {
    return (
        <header className="navigation-bar">
            <h1 className="logo">OFS</h1>
            <SearchBar />
            <div className="profile-container">
                <img className="shopping-cart-icon" src="./src/img/shopping-cart-icon.png" alt="" />
                <img className="profile-icon" src="./src/img/profile-icon.png" alt="" />
            </div>
        </header>
    )
}

export default NavigationBar;