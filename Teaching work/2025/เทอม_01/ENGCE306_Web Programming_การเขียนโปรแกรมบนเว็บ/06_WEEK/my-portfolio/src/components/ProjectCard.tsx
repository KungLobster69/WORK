// src/components/ProjectCard.tsx
interface ProjectCardProps {
  title: string;
  description: string;
  imageUrl: string;
}

function ProjectCard(props: ProjectCardProps) {
  return (
    <div className="project-card">
      <img src={props.imageUrl} alt={props.title} style={{maxWidth: '100%'}} />
      <h3>{props.title}</h3>
      <p>{props.description}</p>
    </div>
  );
}

// function ProjectCard({ title, description, imageUrl }: ProjectCardProps) {
//   return (
//     <div className="project-card">
//       <img src={imageUrl} alt={title} style={{maxWidth: '100%'}} />
//       <h3>{title}</h3>
//       <p>{description}</p>
//     </div>
//   );
// }

export default ProjectCard;