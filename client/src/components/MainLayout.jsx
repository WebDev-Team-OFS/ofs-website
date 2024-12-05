import NavigationBar from './NavigationBar/NavigationBar'
import { Outlet } from 'react-router-dom'
import './main-layout.css'

const MainLayout = () => {
  return (
   <>
    <header>
        <NavigationBar />
    </header>
    <main>
        <Outlet / >
    </main>
    <footer>
        <p>&#xA9; 2024 Online Food Store</p>
        <p><em>*This is a not a real website</em></p>
    </footer>
   </>
  )
}

export default MainLayout;