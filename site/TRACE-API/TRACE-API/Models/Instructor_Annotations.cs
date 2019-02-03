using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace TRACE_API.Models
{
    [MetadataType(typeof(InstructorMetadata))]
    public partial class Instructor
    {
        public string FullName
        {
            get
            {
                return FirstName + ((String.IsNullOrEmpty(MiddleName)) ? " " : " " + MiddleName + " ") + LastName;
            }
        }
    }

    public class InstructorMetadata
    {

    }
}