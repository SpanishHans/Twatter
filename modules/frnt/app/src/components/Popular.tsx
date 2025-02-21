"use client";

import { useState, useEffect } from "react";

const trendingHashtags = [
  "#DramaMinisterial",
  "#CrisisDeGabinete",
  "#MinistroRenuncia",
  "#PolíticaEnCaos",
  "#NuevoGobierno"
];

export default function TrendingCarousel() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prevIndex) => (prevIndex + 1) % trendingHashtags.length);
    }, 3000); // Change text every 3 seconds

    return () => clearInterval(interval); // Cleanup
  }, []);

  return (
      <span className="text-6xl font-bold break-all transition-opacity duration-500">
        {trendingHashtags[index]}
      </span>
  );
}
