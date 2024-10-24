import NavigationBar from "./NavigationBar"
import './landing-page.css'
import GroceryCard from "../GroceryCard"
import FeaturedItems from "./FeaturedItems"


function LandingPage() {
    return (
        <main>
            <NavigationBar />
            <img className="background-image" src="./src/img/landing-page-background.jpg" alt="" />
            <FeaturedItems />
            
        </main>
    )
}

export default LandingPage