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
            <div className="delivery-statement">
                <img className="delivery-image" src="./src/img/delivery.jpg" alt="" />
                <h1>All your <span className="bold">groceries</span> from one place. We deliver <span className="bold">fast</span> and <span className="bold">efficiently</span>.</h1>
            </div>
            <Categories />
            
        </main>
    )
}

export default LandingPage