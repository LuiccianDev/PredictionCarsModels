import React from 'react';
import Hero from '../components/sections/Hero';
import Banner from '../components/sections/Banner';
import Features from '../components/sections/Features';
import LogoCloud from '../components/sections/LogoCloud';
import Prices from '../components/sections/Prices';
import TeamSection from '../components/sections/Team'
import TestimonialsCars from '../components/sections/Testimonials';
import { useAuth } from '../context/AuthContext';

const Home = () => {
  const { user } = useAuth();

  return (
    <main>
      {!user && <Banner />}
      <Hero />
      <Features />
      <LogoCloud />
      <TestimonialsCars />
      <Prices />
      <TeamSection />
    </main>
  );
};

export default Home;
