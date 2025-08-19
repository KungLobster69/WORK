import Header from './components/Header';
import HeroSection from './components/HeroSection';
import AboutMe from './components/AboutMe';
import ProjectList from './components/ProjectList';
import Footer from './components/Footer';
import './App.css'; // Import CSS เพื่อจัดสไตล์

function App() {
  return (
    <div className="container"> {/* ใช้ div ครอบและใส่ className */}
      <Header />
      <main>
        <HeroSection />
        <AboutMe />
        <ProjectList />
      </main>
      <Footer />
    </div>
  );
}

export default App;