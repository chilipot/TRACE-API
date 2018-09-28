using MongoDB.Bson;
using MongoDB.Bson.IO;
using Newtonsoft.Json.Linq;
using System;
using System.Collections.Generic;
using System.Data;
using System.Data.Entity;
using System.Linq;
using System.Net;
using System.Web;
using System.Web.Mvc;
using TRACE_API.Models;
using TRACE_API.Services;

namespace TRACE_API.Controllers
{
    public class ReportsController : Controller
    {
        private DB_A3CB61_TRACE_Entities db = new DB_A3CB61_TRACE_Entities();
        private MongoService mongo = new MongoService();

        // GET: Reports
        [HttpGet]
        public ActionResult Index(int? courseID, int? instructorID, int? termID, int pageNumber = 0, int pageSize = 250, string search = "")
        {
            var reports = db.Reports.AsNoTracking().Include(r => r.Instructor).Include(r => r.Term);

            if (courseID != null)
            {
                reports = reports.Where(r => r.CourseID == courseID);
            }

            if (instructorID != null)
            {
                reports = reports.Where(r => r.InstructorID == instructorID);
            }

            if (termID != null)
            {
                reports = reports.Where(r => r.TermID == termID);
            }

            IOrderedQueryable<Report> results;

            if (!String.IsNullOrWhiteSpace(search))
            {
                search = search.ToUpper();

                var searchWords = search.Split('"')
                     .Select((element, index) => index % 2 == 0  // If even index
                                           ? element.Split(null)  // Split the item
                                           : new string[] { element })  // Keep the entire item
                     .SelectMany(element => element)
                     .Where(x => !String.IsNullOrWhiteSpace(x)).ToArray();

                var subQueries = new List<IQueryable<Report>>();

                foreach (var searchWord in searchWords)
                {
                    subQueries.Add(reports.Where(r => (r.Subject + " " + r.Number + " " + r.Name).ToUpper().Contains(searchWord)));
                    subQueries.Add(reports.Where(r => (r.Instructor.FirstName + " " + r.Instructor.LastName).ToUpper().Contains(searchWord)));
                    subQueries.Add(reports.Where(r => r.Term.Title.ToUpper().Contains(searchWord)));
                }

                var unionResults = subQueries.DefaultIfEmpty().Aggregate((a, b) => a.Concat(b));

                var distinctResults = unionResults.Distinct();
                var unionResultsIDs = unionResults.Select(x => x.ReportID);

                var tolerance = searchWords.Length - 2;

                var filteredDistinctResults = distinctResults.Where(x => unionResultsIDs.Count(y => x.ReportID == y) > tolerance);

                results = filteredDistinctResults.AsQueryable()
                    .OrderByDescending(x => unionResults.Count(y => x.ReportID == y.ReportID))
                    .ThenByDescending(r => r.TermID)
                    .ThenBy(r => (r.Subject + " " + r.Number + " " + r.Name))
                    .ThenBy(r => (r.Instructor.FirstName + " " + r.Instructor.LastName));
            }
            else
            {
                results = reports.OrderByDescending(r => r.TermID)
                    .ThenBy(r => (r.Subject + " " + r.Number + " " + r.Name))
                    .ThenBy(r => (r.Instructor.FirstName + " " + r.Instructor.LastName));
            }

            return View(results.ToPagedList(pageNumber, pageSize));
        }

        [HttpGet]
        public ActionResult Score(int id)
        {
            var report = db.Reports.Find(id);

            if (report == null)
            {
                return HttpNotFound();
            }

            var score = mongo.GetScoreDetails(report.DataID);

            return Content(score.ToJson(), "application/json");
        }
    }
}
