using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace TRACE_API.Models
{
    [MetadataType(typeof(TermMetadata))]
    public partial class Term
    {
        public string NormalizedTitle
        {
            get
            {
                var tokens = Title.Split(":".ToCharArray(), 2);
                return tokens[Math.Min(1, tokens.Length - 1)].Trim();
            }
        }
    }

    public class TermMetadata
    {

    }
}