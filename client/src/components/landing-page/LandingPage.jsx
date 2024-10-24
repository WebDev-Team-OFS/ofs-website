import NavigationBar from "./NavigationBar"
import './landing-page.css'
import FeaturedItems from "./FeaturedItems"
import Categories from "./Categories"


function LandingPage() {
    return (
        <main>
            <NavigationBar />
            <img className="background-image" src="./src/img/landing-page-background.jpg" alt="" />
            <FeaturedItems />
            <div className="row">
                <img src="./src/img/food-variety.jpg" alt="" />
                <h1>We offer a <span className="bold">variety of food</span> variety of food that you can <span className="bold">buy</span> in just a few clicks.</h1>
            </div>
            <Categories />
            <div className="row">
                <h1>All your <span className="bold">groceries</span> from one place. We deliver <span className="bold">fast</span> and <span className="bold">efficiently</span>.</h1>
                <img className="delivery-image" src="./src/img/delivery.jpg" alt="" />
            </div>
            <footer>
                <p>&#xA9; 2024 Online Food Store</p>
                <p><em>*This is a not a real website</em></p>
            </footer>
        </main>
    )
}

export default LandingPage