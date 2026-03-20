import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import HomePage from "./pages/HomePage";
import AboutPage from "./pages/AboutPage";
import MethodologyPage from "./pages/MethodologyPage";
import AboutExtendedPage from "./pages/AboutExtendedPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/analyzer" element={<HomePage />} />
        <Route path="/about-us" element={<AboutPage />} />
        <Route path="/methodology" element={<MethodologyPage />} />
        <Route path="/about" element={<AboutExtendedPage />} />
      </Routes>
    </Router>
  );
}

export default App;
