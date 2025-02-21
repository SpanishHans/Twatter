"use client";

import React, { useState } from "react";
import Button from "./Button"; // Import your button component

const TwattBox: React.FC = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [twatt, setTwatt] = useState(""); // Store the text input

  return (
    <div className="p-4 bg-gray-800 rounded-lg mb-4">
      {/* Textarea (Click to Open Modal) */}
      <textarea
        className="w-full bg-transparent text-white p-2 border border-gray-600 rounded-lg cursor-pointer"
        placeholder="¿Qué está pasando?"
        value={twatt}
        onClick={() => setIsModalOpen(true)} // Open modal on click
        readOnly // Prevent typing directly
      />

      {/* Button (Optional: You can also open the modal from here) */}
      <Button variant="blue" className="mt-2 w-full" onClick={() => setIsModalOpen(true)}>
        Twatt
      </Button>

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
          <div className="bg-gray-900 p-6 rounded-lg w-96">
            <textarea
              className="w-full bg-transparent text-white p-2 border border-gray-600 rounded-lg"
              placeholder="¿Qué está pasando?"
              value={twatt}
              onChange={(e) => setTwatt(e.target.value)} // Update text state
            />
            <div className="flex justify-end mt-4">
              <Button variant="outline" className="mr-2" onClick={() => setIsModalOpen(false)}>
                Cancel
              </Button>
              <Button variant="blue" onClick={() => setIsModalOpen(false)}>
                Twatt
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TwattBox;
