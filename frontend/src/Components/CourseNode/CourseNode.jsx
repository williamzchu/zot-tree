import { useState } from "react";
import "./Course.css";
import axios from "axios";

function Course({ courseId, completionStatus="", specialization=false }) {
  const [id, setId] = useState("");
  const [title, setTitle] = useState("");

  const getCourse = async () => {
    try {
      let res = await axios.get(`${process.env.BACKEND_URL}/course/${courseId}`);
      setId(res.data.payload.id)
      setTitle(res.data.payload.title)
    }
    catch(error) {
      console.error("Error fetching the course data ", error)
    }
  };

  getCourse();

  return (
    <div>
      <div className={`node ${completionStatus} ${specialization ? "specialization" : ""}`}  >
        {id}
        {/* link to more in depth page later i guess */}
      </div>
    </div>
  );
}

export default Course;