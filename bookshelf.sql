sql
\c postgres;
DROP DATABASE articledb;
CREATE DATABASE articledb;
\c articledb;
DROP TABLE comment;
DROP TABLE article;
DROP TABLE author;

table.increments()
table.varchar('first_name', 255).notNullable().defaultTo('')
table.varchar('last_name', 255).notNullable().defaultTo('')
table.varchar('email', 255).notNullable()
table.specificType('hashed_password', 'CHAR(60)').notNullable()

table.dateTime('created_at').notNullable().defaultTo(knex.raw('now()'))
table.dateTime('updated_at').notNullable().defaultTo(knex.raw('now()'))


CREATE TABLE books (
  id serial primary key,
  title varchar(255),
  author varchar(255),
  genre varchar(255),
  description text,
  cover_url text,
  created_at timestamp,
  updated_at timestamp
);
CREATE TABLE users (
  id serial primary key,
  first_name varchar(255),
  last_name varchar(255),
  email varchar(255),
  hashed_password char(60),
  created_at timestamp,
  updated_at timestamp
);
CREATE TABLE favorites (
  id serial primary key,
  book_id integer,
  user_id integer,
  created_at timestamp,
  updated_at timestamp
);

INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('JavaScript, The Good Parts', 'Douglas Crockford', 'JavaScript', 'Most programming languages contain good and bad parts, but JavaScript has more than its share of the bad, having been developed and released in a hurry before it could be refined. This authoritative book scrapes away these bad features to reveal a subset of JavaScript that is more reliable, readable, and maintainable than the language as a whole—a subset you can use to create truly extensible and efficient code.', 'https://students-gschool-production.s3.amazonaws.com/uploads/asset/file/284/javascript_the_good_parts.jpg');


INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('Learning React Native', 'Bonnie Eisenman', 'React', 'Get a practical introduction to React Native, the JavaScript framework for writing and deploying fully featured mobile apps that look and feel native. With this hands-on guide, you will learn how to build applications that target iOS, Android, and other mobile platforms instead of browsers. You will also discover how to access platform features such as the camera, user location, and local storage.','https://students-gschool-production.s3.amazonaws.com/uploads/asset/file/287/learning_react_native.jpg');

INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('Functional JavaScript', 'Michael Fogus', 'JavaScript', 'How can you overcome JavaScript language oddities and unsafe features? With this book, you will learn how to create code that is beautiful, safe, and simple to understand and test by using JavaScript is functional programming support. Author Michael Fogus shows you how to apply functional-style concepts with Underscore.js, a JavaScript library that facilitates functional programming techniques.','https://students-gschool-production.s3.amazonaws.com/uploads/asset/file/297/functional_javascript.jpg');

INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('React: Up & Running', 'Stoyan Stefanov', 'React', 'Hit the ground running with React, the open-source technology from Facebook for building rich web applications fast. With this practical guide, Yahoo! web developer Stoyan Stefanov teaches you how to build components—React is basic building blocks—and organize them into maintainable, large-scale apps. If you are familiar with basic JavaScript syntax, you are ready to get started.','https://students-gschool-production.s3.amazonaws.com/uploads/asset/file/294/react_up_and_running.jpg');

INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('Learning JavaScript Design Patterns', 'Addy Osmani', 'JavaScript', 'With Learning JavaScript Design Patterns, you will learn how to write beautiful, structured, and maintainable JavaScript by applying classical and modern design patterns to the language. If you want to keep your code efficient, more manageable, and up-to-date with the latest best practices, this book is for you.','https://students-gschool-production.s3.amazonaws.com/uploads/asset/file/295/javascript_design_patterns.jpg');

INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('JavaScript with Promises', 'Daniel Parker', 'JavaScript', 'Asynchronous JavaScript is everywhere, whether you are using Ajax, AngularJS, Node.js, or WebRTC. This practical guide shows intermediate to advanced JavaScript developers how Promises can help you manage asynchronous code effectively—including the inevitable flood of callbacks as your codebase grows. You will learn the inner workings of Promises and ways to avoid difficulties and missteps when using them.','https://students-gschool-production.s3.amazonaws.com/uploads/asset/file/296/javascript_with_promises.jpg');

INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('AngularJS: Up and Running', 'Shyam Seshadri', 'Angular', 'If you want to get started with AngularJS, either as a side project, an additional tool, or for your main work, this practical guide teaches you how to use this meta-framework step-by-step, from the basics to advanced concepts. By the end of the book, you will understand how to develop a large, maintainable, and performant application with AngularJS.','http://akamaicovers.oreilly.com/images/0636920033486/lrg.jpg');

INSERT INTO books (title, author, genre, description, cover_url)
  VALUES('Web Development with Node and Express', 'Ethan Brown', 'Node', 'Learn how to build dynamic web applications with Express, a key component of the Node/JavaScript development stack. In this hands-on guide, author Ethan Brown teaches you the fundamentals through the development of a fictional application that exposes a public website and a RESTful API. You will also learn web architecture best practices to help you build single-page, multi-page, and hybrid web apps with Express.','http://akamaicovers.oreilly.com/images/0636920032977/lrg.jpg');

INSERT INTO article (title, body, author_id) VALUES('You will not believe...', 'Biloxi, MS- Local man Ernest Weaver...', 1);
INSERT INTO article (title, body, author_id) VALUES('We dare you to read...', 'A story that will melt your heart with kittens...', 2);
INSERT INTO article (title, body, author_id) VALUES('This is not clickbait', 'Local squirrel wrangler finds himself in a serious situation...', 3);
INSERT INTO comment (name, body, article_id) VALUES('Sally', 'This was very believable.', 1);
INSERT INTO comment (name, body, article_id) VALUES('Abraham', 'I love Biloxi.', 1);
INSERT INTO comment (name, body, article_id) VALUES('Miranda', 'I came for the kittens. I stayed for the prose.', 2);
INSERT INTO comment (name, body, article_id) VALUES('Ezekiel', 'Meh, I like turtles.', 2);
INSERT INTO comment (name, body, article_id) VALUES('Lisa', 'Not impressed. Do it again.', 7);
INSERT INTO author (name) VALUES('E Hemingway');
INSERT INTO author (name) VALUES('W Burroughs');
