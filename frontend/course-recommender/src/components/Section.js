// components/Section.js
import React from 'react';
import Card from './Card';
import TeamBadge from './TeamBadge';
import PriceCard from './PriceCard';
// import './Section.css';
import './../App.css';

const Section = () => {
  return (
    <main>
      <section className="flex-sect">
        <div className="container-width">
          <div className="flex-title">Flex is the new black</div>
          <div className="flex-desc">With flexbox system you're able to build complex layouts easily and with free responsivity</div>
          <div className="cards">
            {[...Array(6)].map((_, i) => (
              <Card key={i} title={`Title ${i + 1}`} subtitle={`Subtitle ${i + 1}`} />
            ))}
          </div>
        </div>
      </section>
      {/* Asset Manager Section */}
      <section className="am-sect">
        <div className="container-width">
          <div className="am-container">
            <img src="/assets/images/demos/phone-app.png" alt="Phone App" className="img-phone" />
            <div className="am-content">
              <div className="am-pre">ASSET MANAGER</div>
              <div className="am-title">Manage your images with Asset Manager</div>
              <div className="am-desc">You can create image blocks with the command from the left panel and edit them with double click</div>
              <div className="am-post">Image uploading is not allowed in this demo</div>
            </div>
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
            <TeamBadge name="Adam Smith" role="CEO" image="/assets/images/demos/team1.jpg" />
            <TeamBadge name="John Black" role="Software Engineer" image="/assets/images/demos/team2.jpg" />
            <TeamBadge name="Jessica White" role="Web Designer" image="/assets/images/demos/team3.jpg" />
          </div>
        </div>
      </section>
    </main>
  );
};

export default Section;
