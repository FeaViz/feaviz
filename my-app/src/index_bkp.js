import React from "react";
import ReactDom from "react-dom";

import "./index.css";

function BookList() {
  return (
    <section className="booklist">
      <Book />
      <Book />
      <Book />
      <Book />
      <Book />
      <Book />
    </section>
  );
}

const ImageBook = () => {
  return (
    <img
      src="https://images-eu.ssl-images-amazon.com/images/I/51b9zA8HjXL.jpg"
      alt=""
    />
  );
};

const TitleBook = () => {
  return <h1>Word Power Made Eas</h1>;
};

const AuthorBook = () => {
  return (
    <h4 style={{ color: "#617d98", fontSize: "0.75rem", marginTop: "0.25rem" }}>
      Norman Lewis
    </h4>
  );
};

const Book = () => {
  return (
    <article className="book">
      <ImageBook />
      <TitleBook />
      <AuthorBook />
    </article>
  );
};

ReactDom.render(<BookList />, document.getElementById("root"));
