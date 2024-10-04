// components/Section.js
import React from 'react';
import Card from './Card';
import TeamBadge from './TeamBadge';
import PriceCard from './PriceCard';
import CourseInput from './CourseInput';
import './../App.css';
import deveoper_icon from './../images/Frontend_Developer_Icon.jpg';
import computer_icon from './../images/Computer_Icon.jpg'

const Section = () => {
  return (
    <main>
      <section className="flex-sect">
        <div className="container-width">
            <CourseInput />
        </div>
      </section>
      <section className="am-sect">
        <div className="container-width">
        <div className="flex-title">Explore These Courses</div>
          <div className="flex-desc">The following courses might be helpful for your future study</div>
          <div className="cards">
            {[...Array(6)].map((_, i) => (
              <Card key={i} title={`Title ${i + 1}`} subtitle={`Subtitle ${i + 1}`} />
            ))}
          </div>
        </div>
      </section>
      {/* Price Cards Section */}
      <section className="blk-sect">
        <div className="container-width">
          <div className="blk-title">Blocks</div>
          <div className="blk-desc">Each element in HTML page could be seen as a block...</div>
          <div className="price-cards">
            <PriceCard title="Starter" description="Some random list" price="$9.90/mo" />
            <PriceCard title="Regular" description="Some random list" price="$19.90/mo" />
            <PriceCard title="Enterprise" description="Some random list" price="$29.90/mo" />
          </div>
        </div>
      </section>
      {/* Team Section */}
      <section className="bdg-sect">
        <div className="container-width">
          <h1 className="bdg-title">The team</h1>
          <div className="badges">
            <TeamBadge 
                name="Haoran Zhao " 
                role="Software Engineer" 
                image={deveoper_icon}
                description="The database wizard, conjuring up magical data structures that keep everything running smoothly!"/>
            <TeamBadge 
                name="Jinyang Zhao" 
                role="Software Engineer" 
                image={deveoper_icon}
                description="The frontend developer crafting sleek and user-friendly interfaces."/>
            <TeamBadge 
                name="Xiao Hu" 
                role="Software Engineer"
                image={deveoper_icon}
                description="The AI specialist designing smart models to enhance our project’s capabilities."/>
            <TeamBadge 
                name="Jiantong Lyu" 
                role="Software Engineer"
                image={deveoper_icon}
                description="The database analyst ensuring our data is organized and efficient."/>
            <TeamBadge 
                name="Paul Tang" 
                role="Software Engineer"
                image={deveoper_icon}
                description="The AI model expert helping to bring intelligent solutions to the table"/>
            <TeamBadge 
                name="ChatGPT" 
                role="Software Engineer"
                image={computer_icon}
                description="Our witty virtual assistant, we can't live without it!"/>
          </div>
        </div>
      </section>
    </main>
  );
};

export default Section;