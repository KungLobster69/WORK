import React from 'react';

interface SectionProps {
  title: string;
  children: React.ReactNode;
  id?: string;
}

function Section({ title, children, id }: SectionProps) {
  return (
    <section id={id}>
      <h2>{title}</h2>
      {children}
    </section>
  );
}
export default Section;