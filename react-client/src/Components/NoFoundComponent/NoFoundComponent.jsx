import React, { useState, useEffect } from "react";
import "./NoFoundComponent.css";

export const NoFoundComponent = () => {
  return (
    <>
      <div className="sorry-wrapper">
        <h1>Sorry!</h1>
        <h2>The page you are looking for is not found!</h2>
      </div>
    </>
  );
};
