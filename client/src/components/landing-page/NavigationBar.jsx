

function NavigationBar() {
    return (
        <header className="navigation-bar">
            <h1 className="logo">OFS</h1>
            <div className="search-bar">
                <input type="text" className="search-input" placeholder="Search Groceries"/>
                <img src="./src/img/search-icon.png" alt="" className="search-icon" />
            </div>
            <div className="profile-container">
                <img className="shopping-cart-icon" src="./src/img/shopping-cart-icon.png" alt="" />
                <img className="profile-icon" src="./src/img/profile-icon.png" alt="" />
            </div>
        </header>
    )
}

export default NavigationBar;