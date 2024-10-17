import NavigationBar from "./NavigationBar"
import './landing-page.css'
function LandingPage() {
    return (
        <main>
            <NavigationBar />
            <img className="background-image" src="./src/img/landing-page-background.jpg" alt="" />
            <div class="container">
                <h1>Featured Items</h1>
            </div>
            
        </main>
    )
}

export default LandingPage