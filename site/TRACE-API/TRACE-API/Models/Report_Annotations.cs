using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.ComponentModel.DataAnnotations;
using System.IO;

namespace TRACE_API.Models
{
    [MetadataType(typeof(ReportMetadata))]
    public partial class Report
    {
        public string FullCourseName
        {
            get
            {
                return Subject + " " + Number + " - " + Name;
            }
        }
    }

    public class ReportMetadata
    {

    }
}