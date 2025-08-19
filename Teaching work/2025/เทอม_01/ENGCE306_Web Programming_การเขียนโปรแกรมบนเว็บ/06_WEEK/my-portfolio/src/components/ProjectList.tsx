// function ProjectList() {
//   return (
//     <section id="projects">
//       <h2>My Projects</h2>
//       <div>
//         <p>Project 1 details will go here...</p>
//         <p>Project 2 details will go here...</p>
//       </div>
//     </section>
//   );
// }
// export default ProjectList;

// src/components/ProjectList.tsx
import ProjectCard from './ProjectCard'; // 1. Import เข้ามา

// 2. เตรียมข้อมูล (ปกติข้อมูลจะมาจาก API แต่ตอนนี้เราจำลองขึ้นมาก่อน)
const projects = [
  {
    id: 1,
    title: 'Portfolio Website',
    description: 'Built with React and TypeScript for ENGCE306.',
    imageUrl: 'https://placehold.co/600x400?text=Project+1'
  },
  {
    id: 2,
    title: 'Database Management System',
    description: 'A project from ENGCE126 course.',
    imageUrl: 'https://placehold.co/600x400?text=Project+2'
  }
];

function ProjectList() {
  return (
    <section id="projects">
      <h2>My Projects</h2>
      <div>
        {/* 3. ใช้ .map() เพื่อสร้าง ProjectCard จากข้อมูล */}
        {projects.map(project => (
          <ProjectCard
            key={project.id}
            title={project.title}
            description={project.description}
            imageUrl={project.imageUrl}
          />
        ))}
      </div>
    </section>
  );
}

export default ProjectList;