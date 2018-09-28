using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace TRACE_API.Services
{
    public static class ExtensionMethods
    {
        public static List<T> ToPagedList<T>(this IOrderedQueryable<T> list, int pageNumber, int pageSize)
        {
            int skipVal = (pageNumber == 0) ? 0 : ((pageNumber * pageSize) - 1);
            return list.Skip(skipVal).Take(pageSize).ToList();
        }
    }
}